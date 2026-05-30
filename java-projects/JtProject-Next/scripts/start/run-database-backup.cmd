@echo off
setlocal

cd /d "%~dp0\..\.."

echo ========================================
echo JtSpringProject - BAT-007 Database Backup
echo ========================================
echo.
echo Profile  : batch
echo Job Name : databaseBackup
echo.

if exist mvnw.cmd (
  call mvnw.cmd -DskipTests compile org.codehaus.mojo:exec-maven-plugin:3.5.0:java -Dexec.mainClass=com.jtspringproject.JtSpringProject.batch.launcher.DatabaseBackupBatchApplication
) else (
  call mvn -DskipTests compile org.codehaus.mojo:exec-maven-plugin:3.5.0:java -Dexec.mainClass=com.jtspringproject.JtSpringProject.batch.launcher.DatabaseBackupBatchApplication
)

exit /b %ERRORLEVEL%
