これどういう状況？

```shell
langchainmaru@maru-home:~/py/langchain$ uv run mcp/hello_mcp_server.py
^C^CTraceback (most recent call last):
  File "/home/maru/py/langchain/mcp/hello_mcp_server.py", line 76, in <module>
    asyncio.run(main())
  File "/home/maru/.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/asyncio/runners.py", line 195, in run
    return runner.run(main)
           ^^^^^^^^^^^^^^^^
  File "/home/maru/.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/asyncio/runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/maru/.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/asyncio/base_events.py", line 678, in run_until_complete
    self.run_forever()
  File "/home/maru/.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/asyncio/base_events.py", line 645, in run_forever
    self._run_once()
  File "/home/maru/.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/asyncio/base_events.py", line 1961, in _run_once
    event_list = self._selector.select(timeout)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/maru/.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/selectors.py", line 468, in select
    fd_event_list = self._selector.poll(timeout, max_ev)
                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/maru/.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/asyncio/runners.py", line 157, in _on_sigint
    raise KeyboardInterrupt()
KeyboardInterrupt
^CException ignored in: <module 'threading' from '/home/maru/.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/threading.py'>
Traceback (most recent call last):
  File "/home/maru/.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/threading.py", line 1624, in _shutdown
    lock.acquire()
KeyboardInterrupt:
```
