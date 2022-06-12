#build an sdist (source distribution) package for vocola (vocola2)
#no wheel is built, one less thing to worry about
#use the no-setup option, which requires a 
flit publish  --format sdist  --no-setup-py  --repository pypi