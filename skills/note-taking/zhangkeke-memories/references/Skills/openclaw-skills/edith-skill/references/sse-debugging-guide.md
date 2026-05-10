# SSE (Server-Sent Events) Debugging Guide

## Quick Diagnosis

When the visualization panel loads but doesn't respond to interactions:

```javascript
// Paste in browser console
console.log('=== SSE Debug ===');
console.log('EventSource:', typeof EventSource);
var es = new EventSource('/stream');
console.log('readyState:', es.readyState);  // 0=CONNECTING, 1=OPEN, 2=CLOSED
es.onopen = () => console.log('SSE opened');
es.onerror = (e) => console.log('SSE error:', e);
es.onmessage = (e) => console.log('SSE data:', e.data);
```

## readyState Values

| Value | Name | Meaning |
|-------|------|---------|
| 0 | CONNECTING | Reconnecting or first connect |
| 1 | OPEN | Connection established |
| 2 | CLOSED | Connection failed permanently |

## Common Failure Patterns

### 1. readyState stays at 0 (CONNECTING)

**Symptoms**: UI loads, buttons clickable, but no state updates

**Causes**:
- Flask server not running
- Wrong port (check `lsof -i :8080`)
- CORS issues (if cross-origin)
- Proxy blocking SSE

**Fix**:
```bash
# Check server
lsof -i :8080 | grep LISTEN

# Test SSE endpoint directly
curl -s -N http://localhost:8080/stream | head -3
```

### 2. SSE connects but no data received

**Symptoms**: readyState=1, but `es.onmessage` never fires

**Causes**:
- Server not sending events
- Queue not processing
- State not changing (nothing to send)

**Fix**:
```javascript
// Test with manual API call to trigger state change
fetch('/api/phase', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({phase:'understand'})})
```

### 3. Intermittent disconnections

** Symptoms**: SSE connects, works briefly, then stops

**Causes**:
- Long polling timeout
- Server restart
- Network interruption

**Fix**: Add reconnection logic with exponential backoff

## Fallback: Polling Mode

When SSE fails, use polling:

```javascript
function startPolling(interval) {
  setInterval(() => {
    fetch('/api/state')
      .then(r => r.json())
      .then(data => updateUI(data))
      .catch(e => console.error('Poll failed:', e));
  }, interval || 2000);
}

// Usage
if (es.readyState === 2) {  // CLOSED
  startPolling();
}
```

## Server-Side SSE Format

Flask SSE endpoint should return:

```python
@app.route("/stream")
def stream():
    def gen():
        q = state.add_client()
        try:
            while True:
                data = q.get()  # Blocks until new data
                yield f"data: {json.dumps(data)}\n\n"
        except GeneratorExit:
            state.clients.remove(q)
    return Response(gen(), mimetype="text/event-stream")
```

## Verification Checklist

- [ ] Server running and port open
- [ ] `/api/state` returns valid JSON
- [ ] `/stream` returns `text/event-stream` content-type
- [ ] Browser console shows no CORS errors
- [ ] `es.readyState` reaches 1 (OPEN)
- [ ] `es.onmessage` fires when state changes
