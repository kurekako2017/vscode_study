@echo off
setlocal

cd /d "%~dp0\..\.."

echo ========================================
echo JtSpringProject - BAT-006 Cart Residual Inventory
echo ========================================
echo.
echo Profile  : batch
echo Job Name : cartResidualInventory
echo.

if exist mvnw.cmd (
  call mvnw.cmd -DskipTests compile org.codehaus.mojo:exec-maven-plugin:3.5.0:java -Dexec.mainClass=com.jtspringproject.JtSpringProject.batch.launcher.CartResidualInventoryBatchApplication
) else (
  call mvn -DskipTests compile org.codehaus.mojo:exec-maven-plugin:3.5.0:java -Dexec.mainClass=com.jtspringproject.JtSpringProject.batch.launcher.CartResidualInventoryBatchApplication
)

exit /b %ERRORLEVEL%
