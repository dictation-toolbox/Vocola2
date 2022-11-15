from pathlib import Path
import pytest
from natlinkcore import natlinkstatus
from natlinkcore.loader import *

status = natlinkstatus.NatlinkStatus()

thisDir = Path(__file__).parent
thisFileName = Path(__file__).stem + ".py"


## taken from natlinkcore, test_loader:

class MockLoggingHandler(logging.Handler):
    """Mock logging handler to check for expected logs."""

    def __init__(self, *args, **kwargs):
        self.messages: Dict[str, List[str]] = {}
        self.reset()
        logging.Handler.__init__(self, *args, **kwargs)

    def emit(self, record):
        self.messages[record.levelname.lower()].append(record.getMessage())

    def reset(self):
        self.messages = {
            'debug': [],
            'info': [],
            'warning': [],
            'error': [],
            'critical': [],
        }

@pytest.fixture()
def empty_config():
    config = NatlinkConfig.get_default_config()
    return config

@pytest.fixture()
def logger():
    _logger = logging.Logger('natlink')
    _logger.setLevel(logging.DEBUG)
    log_handler = MockLoggingHandler()
    _logger.addHandler(log_handler)
    _logger.messages = log_handler.messages
    _logger.reset = lambda: log_handler.reset()
    return _logger

## comment out one of the two functions...
def test_get_content_new_vcl_file_true_true(empty_config, logger, monkeypatch):
    """see if the header of a new _vcl_file is correct with the options
    
    here text, because vocola takes languages and different language (abc),
    and include li
    """
    # patching the language property
    main = NatlinkMain(logger, empty_config)
    main.config = empty_config
    main.language = 'abc'
    assert main.language == 'abc'
    monkeypatch.setattr(main, "trigger_load", lambda: None)

    monkeypatch.setattr(status, "getVocolaTakesUnimacroActions", lambda: True)
    monkeypatch.setattr(status, "getVocolaTakesLanguages", lambda: True)
    from vocola2 import _vocola_main
    voc_main = _vocola_main.ThisGrammar()
    after_text = voc_main.get_after_comment_new_vcl_file()
    assert after_text == ' (language: abc)\ninclude ..\\Unimacro.vch;\n\n'

# def test_get_content_new_vcl_file_enx_false_false(empty_config, logger, monkeypatch):
#     """see if the header of a new _vcl_file is correct with the options
#     
#     here no extra content, with language enx, no unimacro actions and also no vocola takes languages
#     """
#     # patching the language property
#     main = NatlinkMain(logger, empty_config)
#     main.config = empty_config
#     main.language = 'enx'
#     assert main.language == 'enx'
#     monkeypatch.setattr(main, "trigger_load", lambda: None)
# 
#     monkeypatch.setattr(status, "getVocolaTakesUnimacroActions", lambda: False)
#     monkeypatch.setattr(status, "getVocolaTakesLanguages", lambda: False)
#     from vocola2 import _vocola_main
#     voc_main = _vocola_main.ThisGrammar()
#     after_text = voc_main.get_after_comment_new_vcl_file()
#     assert after_text == '\n\n'
#     
    
    
    
    
if __name__ == "__main__":
    pytest.main([__file__])
