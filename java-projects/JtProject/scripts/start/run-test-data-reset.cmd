@echo off
setlocal

cd /d "%~dp0\..\.."

echo ========================================
echo JtSpringProject - BAT-003 Test Data Reset
echo ========================================
echo.
echo Profile  : batch
echo Job Name : testDataReset
echo.

if exist mvnw.cmd (
  call mvnw.cmd -DskipTests compile org.codehaus.mojo:exec-maven-plugin:3.5.0:java -Dexec.mainClass=com.jtspringproject.JtSpringProject.batch.TestDataResetBatchApplication
) else (
  call mvn -DskipTests compile org.codehaus.mojo:exec-maven-plugin:3.5.0:java -Dexec.mainClass=com.jtspringproject.JtSpringProject.batch.TestDataResetBatchApplication
)

exit /b %ERRORLEVEL%
