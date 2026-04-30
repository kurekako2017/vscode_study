@echo off
setlocal

cd /d "%~dp0\..\.."

echo ========================================
echo JtSpringProject - BAT-004 App Log Rotation
echo ========================================
echo.
echo Profile  : batch
echo Job Name : appLogRotation
echo.

if exist mvnw.cmd (
  call mvnw.cmd -DskipTests compile org.codehaus.mojo:exec-maven-plugin:3.5.0:java -Dexec.mainClass=com.jtspringproject.JtSpringProject.batch.AppLogRotationBatchApplication
) else (
  call mvn -DskipTests compile org.codehaus.mojo:exec-maven-plugin:3.5.0:java -Dexec.mainClass=com.jtspringproject.JtSpringProject.batch.AppLogRotationBatchApplication
)

exit /b %ERRORLEVEL%
