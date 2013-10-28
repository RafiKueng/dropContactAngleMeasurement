@echo ################################
@echo # starting rendering           #
@echo ################################

cd _scripts
convert_odg.py
::render_seq.py
render_code.py
render_uml.py

@echo #
@echo # rendering finished
@echo ################################