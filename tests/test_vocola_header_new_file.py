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
def test_get_content_new_vcl_file(empty_config, logger, monkeypatch):
    """see if the header of a new _vcl_file is correct with the options
    
    """
    # patching the language property
    main = NatlinkMain(logger, empty_config)
    main.config = empty_config
    main.language = 'enx'
    assert main.language == 'enx'
    # main.language = 'nld'
    # assert main.language == 'nld'
    
    ## after this setting and imports of voc_main, the setting is not affected any more...
    ## language is a property in main (loader.NatlinkMain) and natlinkstatus.NatlinkStatus() (linked to main).
    ## so first test with lines 59 and 60 commented, testing 'enx'.
    ## then uncomment these 2 lines, and test with 'nld', which stands for every language being not 'enx'
    
    monkeypatch.setattr(main, "trigger_load", lambda: None)

    from vocola2 import _vocola_main
    voc_main = _vocola_main.ThisGrammar()

    ## True, True, different result for 'enx' and other languages:
    monkeypatch.setattr(status, "getVocolaTakesUnimacroActions", lambda: True)
    monkeypatch.setattr(status, "getVocolaTakesLanguages", lambda: True)

    after_text = voc_main.get_after_comment_new_vcl_file()
    if main.language == 'enx':
        assert after_text == '\ninclude Unimacro.vch;\n\n'
    else:
        assert after_text == ' (language: nld)\ninclude ..\\Unimacro.vch;\n\n'

    
    ## False, False, same for different languages as set above.
    monkeypatch.setattr(status, "getVocolaTakesUnimacroActions", lambda: False)
    monkeypatch.setattr(status, "getVocolaTakesLanguages", lambda: False)
    after_text = voc_main.get_after_comment_new_vcl_file()
    assert after_text == '\n\n'

    # same for different languages:
    monkeypatch.setattr(status, "getVocolaTakesUnimacroActions", lambda: True)
    monkeypatch.setattr(status, "getVocolaTakesLanguages", lambda: False)
    after_text = voc_main.get_after_comment_new_vcl_file()
    assert after_text == '\ninclude Unimacro.vch;\n\n'

    ## different for 'enx' and other languages:
    monkeypatch.setattr(status, "getVocolaTakesUnimacroActions", lambda: False)
    monkeypatch.setattr(status, "getVocolaTakesLanguages", lambda: True)
    after_text = voc_main.get_after_comment_new_vcl_file()
    if main.language == 'enx':
        assert after_text == '\n\n'
    else:
        assert after_text == ' (language: nld)\n\n'
        
    
    
    
     
    
    
    
    
if __name__ == "__main__":
    pytest.main([__file__])
