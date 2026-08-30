#!/usr/bin/env bash
# Start the brainstorm server and output connection info
# Usage: start-server.sh [--project-dir <path>] [--host <bind-host>] [--url-host <display-host>] [--foreground] [--background]
#
# Starts server on a random high port, outputs JSON with URL.
# Each session gets its own directory to avoid conflicts.
#
# Options:
#   --project-dir <path>  Store visual content under
#                         <path>/.enterprise-dev-workflow/brainstorm/.
#                         Authentication state stays in the OS runtime/temp area.
#   --host <bind-host>    Host/interface to bind (default: 127.0.0.1).
#                         Use 0.0.0.0 in remote/containerized environments.
#   --url-host <host>     Hostname shown in returned URL JSON.
#   --idle-timeout-minutes <n>  Shut down after n minutes idle (default 240 = 4h).
#   --open                Auto-open the browser on the first screen (use only
#                         after the user approves the visual companion).
#   --foreground          Run server in the current terminal (no backgrounding).
#   --background          Force background mode (overrides Codex auto-foreground).

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Parse arguments
PROJECT_DIR=""
FOREGROUND="false"
FORCE_BACKGROUND="false"
BIND_HOST="127.0.0.1"
URL_HOST=""
IDLE_TIMEOUT_MINUTES=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --project-dir)
      PROJECT_DIR="$2"
      shift 2
      ;;
    --host)
      BIND_HOST="$2"
      shift 2
      ;;
    --url-host)
      URL_HOST="$2"
      shift 2
      ;;
    --idle-timeout-minutes)
      IDLE_TIMEOUT_MINUTES="$2"
      shift 2
      ;;
    --open)
      export BRAINSTORM_OPEN=1
      shift
      ;;
    --foreground|--no-daemon)
      FOREGROUND="true"
      shift
      ;;
    --background|--daemon)
      FORCE_BACKGROUND="true"
      shift
      ;;
    *)
      echo "{\"error\": \"Unknown argument: $1\"}"
      exit 1
      ;;
  esac
done

if [[ -z "$URL_HOST" ]]; then
  if [[ "$BIND_HOST" == "127.0.0.1" || "$BIND_HOST" == "localhost" ]]; then
    URL_HOST="localhost"
  else
    URL_HOST="$BIND_HOST"
  fi
fi

if [[ -n "$IDLE_TIMEOUT_MINUTES" ]]; then
  if ! [[ "$IDLE_TIMEOUT_MINUTES" =~ ^[0-9]+$ ]] || [[ "$IDLE_TIMEOUT_MINUTES" -lt 1 ]]; then
    echo "{\"error\": \"--idle-timeout-minutes must be a positive integer\"}"
    exit 1
  fi
  export BRAINSTORM_IDLE_TIMEOUT_MS=$(( IDLE_TIMEOUT_MINUTES * 60 * 1000 ))
fi

is_windows_like_shell() {
  case "${OSTYPE:-}" in
    msys*|cygwin*|mingw*) return 0 ;;
  esac
  if [[ -n "${MSYSTEM:-}" ]]; then
    return 0
  fi
  local uname_s
  uname_s="$(uname -s 2>/dev/null || true)"
  case "$uname_s" in
    MSYS*|MINGW*|CYGWIN*) return 0 ;;
  esac
  return 1
}

# Some environments reap detached/background processes. Auto-foreground when detected.
if [[ -n "${CODEX_CI:-}" && "$FOREGROUND" != "true" && "$FORCE_BACKGROUND" != "true" ]]; then
  FOREGROUND="true"
fi

# Windows/Git Bash reaps nohup background processes. Auto-foreground when detected.
if [[ "$FOREGROUND" != "true" && "$FORCE_BACKGROUND" != "true" ]]; then
  if is_windows_like_shell; then
    FOREGROUND="true"
  fi
fi

# Runtime files (server.log and server-info) may embed the session key —
# keep them outside the consuming project and owner-only.
umask 077

if [[ -n "$PROJECT_DIR" ]]; then
  if ! PROJECT_DIR="$(cd "$PROJECT_DIR" 2>/dev/null && pwd -P)"; then
    echo '{"error": "--project-dir must name an existing directory"}'
    exit 1
  fi
  BRAINSTORM_PROJECT_BASE="${PROJECT_DIR}/.enterprise-dev-workflow/brainstorm"
  if [[ -L "${PROJECT_DIR}/.enterprise-dev-workflow" || -L "$BRAINSTORM_PROJECT_BASE" ]]; then
    echo '{"error": "refusing symlinked project content directory"}'
    exit 1
  fi
  if ! mkdir -p "$BRAINSTORM_PROJECT_BASE"; then
    echo '{"error": "failed to create project content directory"}'
    exit 1
  fi
  if [[ -L "$BRAINSTORM_PROJECT_BASE" || ! -d "$BRAINSTORM_PROJECT_BASE" || ! -O "$BRAINSTORM_PROJECT_BASE" ]]; then
    echo '{"error": "project content directory ownership check failed"}'
    exit 1
  fi
  if ! BRAINSTORM_PROJECT_BASE="$(cd "$BRAINSTORM_PROJECT_BASE" 2>/dev/null && pwd -P)"; then
    echo '{"error": "failed to resolve project content directory"}'
    exit 1
  fi
  case "${BRAINSTORM_PROJECT_BASE}/" in
    "${PROJECT_DIR}/"*) ;;
    *) echo '{"error": "project content directory escaped --project-dir"}'; exit 1 ;;
  esac
  if ! BRAINSTORM_CONTENT_SESSION="$(mktemp -d "${BRAINSTORM_PROJECT_BASE%/}/session.XXXXXXXX")"; then
    echo '{"error": "failed to create private project content session"}'
    exit 1
  fi
  if [[ -L "$BRAINSTORM_CONTENT_SESSION" || ! -d "$BRAINSTORM_CONTENT_SESSION" || ! -O "$BRAINSTORM_CONTENT_SESSION" ]] \
      || ! chmod 700 "$BRAINSTORM_CONTENT_SESSION"; then
    echo '{"error": "failed to secure project content session"}'
    exit 1
  fi
  CONTENT_DIR="${BRAINSTORM_CONTENT_SESSION}/content"
fi

# Create a new unpredictable, owner-only runtime directory for every launch.
# Do not persist bearer keys or ports between launches: rotation is safer than
# seamless reconnection, and avoids predictable shared-/tmp state.
BRAINSTORM_RUNTIME_BASE="${XDG_RUNTIME_DIR:-${TMPDIR:-/tmp}}"
case "$BRAINSTORM_RUNTIME_BASE" in
  /*) ;;
  *) echo '{"error": "runtime/temp directory must be an absolute path"}'; exit 1 ;;
esac
if ! BRAINSTORM_RUNTIME_BASE="$(cd "$BRAINSTORM_RUNTIME_BASE" 2>/dev/null && pwd -P)"; then
  echo '{"error": "runtime/temp directory does not exist"}'
  exit 1
fi
if [[ -n "$PROJECT_DIR" ]]; then
  case "${BRAINSTORM_RUNTIME_BASE}/" in
    "${PROJECT_DIR}/"*) echo '{"error": "runtime/temp directory must be outside --project-dir"}'; exit 1 ;;
  esac
fi
if ! BRAINSTORM_RUNTIME_DIR="$(mktemp -d "${BRAINSTORM_RUNTIME_BASE%/}/enterprise-dev-workflow-brainstorm.XXXXXXXX")"; then
  echo '{"error": "failed to create private runtime directory"}'
  exit 1
fi
if [[ -L "$BRAINSTORM_RUNTIME_DIR" || ! -d "$BRAINSTORM_RUNTIME_DIR" || ! -O "$BRAINSTORM_RUNTIME_DIR" ]]; then
  echo '{"error": "runtime directory ownership check failed"}'
  exit 1
fi
if ! chmod 700 "$BRAINSTORM_RUNTIME_DIR"; then
  echo '{"error": "failed to secure runtime directory"}'
  exit 1
fi
SESSION_DIR="$BRAINSTORM_RUNTIME_DIR"
if [[ -z "$PROJECT_DIR" ]]; then
  CONTENT_DIR="${SESSION_DIR}/content"
fi

STATE_DIR="${SESSION_DIR}/state"
PID_FILE="${STATE_DIR}/server.pid"
LOG_FILE="${STATE_DIR}/server.log"
SERVER_ID_FILE="${STATE_DIR}/server-instance-id"

# Create persistent visual content separately from transient authenticated state.
if ! mkdir -p "$CONTENT_DIR" "$STATE_DIR"; then
  echo '{"error": "failed to create content or runtime state directory"}'
  exit 1
fi
if [[ -n "${BRAINSTORM_CONTENT_SESSION:-}" ]]; then
  BRAINSTORM_IGNORE_FILE="${BRAINSTORM_CONTENT_SESSION}/.gitignore"
  if ! printf '*\n' > "$BRAINSTORM_IGNORE_FILE"; then
    echo '{"error": "failed to create content-session ignore rule"}'
    exit 1
  fi
fi

SERVER_ID=""
if [[ -r /dev/urandom ]]; then
  SERVER_ID="$(od -An -N24 -tx1 /dev/urandom 2>/dev/null | tr -d ' \n' || true)"
fi
if ! [[ "$SERVER_ID" =~ ^[A-Za-z0-9_-]{32,64}$ ]]; then
  SERVER_ID="$(printf '%08x%08x%08x%08x' "$$" "$(date +%s)" "${RANDOM:-0}" "${RANDOM:-0}")"
fi
if ! printf '%s\n' "$SERVER_ID" > "$SERVER_ID_FILE" || ! chmod 600 "$SERVER_ID_FILE"; then
  echo '{"error": "failed to secure server instance metadata"}'
  exit 1
fi

# Kill any existing server
if [[ -f "$PID_FILE" ]]; then
  old_pid=$(cat "$PID_FILE")
  kill "$old_pid" 2>/dev/null
  rm -f "$PID_FILE"
fi

cd "$SCRIPT_DIR" || exit 1

# Resolve the harness PID (grandparent of this script).
# $PPID is the ephemeral shell the harness spawned to run us — it dies
# when this script exits. The harness itself is $PPID's parent.
OWNER_PID="$(ps -o ppid= -p "$PPID" 2>/dev/null | tr -d ' ')"
if [[ -z "$OWNER_PID" || "$OWNER_PID" == "1" ]]; then
  OWNER_PID="$PPID"
fi

# Windows/MSYS2: Node.js cannot see POSIX PIDs from the MSYS2 namespace.
# Passing a PID node cannot verify causes server to log owner-pid-invalid
# and self-terminate at the 60-second lifecycle check. Clear it so the
# watchdog is disabled and the idle timeout becomes the only shutdown trigger.
if is_windows_like_shell; then
  OWNER_PID=""
fi

# Foreground mode for environments that reap detached/background processes.
if [[ "$FOREGROUND" == "true" ]]; then
  env BRAINSTORM_DIR="$SESSION_DIR" BRAINSTORM_CONTENT_DIR="$CONTENT_DIR" BRAINSTORM_HOST="$BIND_HOST" BRAINSTORM_URL_HOST="$URL_HOST" BRAINSTORM_OWNER_PID="$OWNER_PID" node server.cjs "--brainstorm-server-id=$SERVER_ID" &
  SERVER_PID=$!
  echo "$SERVER_PID" > "$PID_FILE"
  wait "$SERVER_PID"
  exit $?
fi

# Start server, capturing output to log file
# Use nohup to survive shell exit; disown to remove from job table
nohup env BRAINSTORM_DIR="$SESSION_DIR" BRAINSTORM_CONTENT_DIR="$CONTENT_DIR" BRAINSTORM_HOST="$BIND_HOST" BRAINSTORM_URL_HOST="$URL_HOST" BRAINSTORM_OWNER_PID="$OWNER_PID" node server.cjs "--brainstorm-server-id=$SERVER_ID" > "$LOG_FILE" 2>&1 &
SERVER_PID=$!
disown "$SERVER_PID" 2>/dev/null
echo "$SERVER_PID" > "$PID_FILE"

# Wait for server-started message (check log file)
for _ in {1..50}; do
  if grep -q "server-started" "$LOG_FILE" 2>/dev/null; then
    # Verify server is still alive after a short window (catches process reapers)
    alive="true"
    for _ in {1..20}; do
      if ! kill -0 "$SERVER_PID" 2>/dev/null; then
        alive="false"
        break
      fi
      sleep 0.1
    done
    if [[ "$alive" != "true" ]]; then
      echo "{\"error\": \"Server started but was killed. Retry in a persistent terminal with: $SCRIPT_DIR/start-server.sh${PROJECT_DIR:+ --project-dir $PROJECT_DIR} --host $BIND_HOST --url-host $URL_HOST --foreground\"}"
      exit 1
    fi
    grep "server-started" "$LOG_FILE" | head -1
    # The caller now has the connection JSON. Remove the bearer key from the
    # persistent log while leaving the file available for later diagnostics.
    : > "$LOG_FILE"
    exit 0
  fi
  sleep 0.1
done

# Timeout - server didn't start
echo '{"error": "Server failed to start within 5 seconds"}'
exit 1
