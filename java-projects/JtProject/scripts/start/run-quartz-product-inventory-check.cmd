@echo off
setlocal

cd /d "%~dp0\..\.."

echo ========================================
echo JtSpringProject - Quartz Product Inventory Check
echo ========================================
echo.
echo Profiles : batch, quartz-lab
echo Job Name : productInventoryCheckQuartzJob
echo Mode     : repeat scheduler
echo Stop     : Ctrl+C
echo.

if exist mvnw.cmd (
  call mvnw.cmd -q -DskipTests compile org.codehaus.mojo:exec-maven-plugin:3.5.0:java -Dexec.mainClass=com.jtspringproject.JtSpringProject.batch.quartz.QuartzProductInventoryCheckApplication
  if %ERRORLEVEL% EQU 0 exit /b 0
  echo mvnw.cmd failed. Falling back to mvn.
)

call mvn -q -DskipTests compile org.codehaus.mojo:exec-maven-plugin:3.5.0:java -Dexec.mainClass=com.jtspringproject.JtSpringProject.batch.quartz.QuartzProductInventoryCheckApplication

exit /b %ERRORLEVEL%
