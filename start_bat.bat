@echo off
if "%1" == "h" goto begin
mshta vbscript:createobject("wscript.shell").run("""%~0"" h",0)(window.close)&&exit
:begin

D: & cd D:\Data_upload_tool &call .venv\Scripts\activate.bat

python BVPP_Server.py


