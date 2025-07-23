import asyncio
import pytest

def pytest_configure(config):
    config.addinivalue_line('markers', 'asyncio: mark test to run with asyncio')

@pytest.hookimpl(tryfirst=True)
def pytest_pyfunc_call(pyfuncitem):
    if 'asyncio' in pyfuncitem.keywords:
        loop = asyncio.new_event_loop()
        try:
            loop.run_until_complete(pyfuncitem.obj(**pyfuncitem.funcargs))
        finally:
            loop.close()
        return True
