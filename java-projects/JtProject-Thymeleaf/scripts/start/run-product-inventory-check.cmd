@echo off
setlocal

cd /d "%~dp0\..\.."

echo ========================================
echo JtSpringProject - Product Inventory Check Batch
echo ========================================
echo.
echo Profile  : batch
echo Job Name : productInventoryCheck
echo Output   : batch-output
echo.

if exist mvnw.cmd (
  call mvnw.cmd -DskipTests compile org.codehaus.mojo:exec-maven-plugin:3.5.0:java -Dexec.mainClass=com.jtspringproject.JtSpringProject.batch.ProductInventoryCheckBatchApplication -Dexec.args=--batch.jobName=productInventoryCheck
) else (
  call mvn -DskipTests compile org.codehaus.mojo:exec-maven-plugin:3.5.0:java -Dexec.mainClass=com.jtspringproject.JtSpringProject.batch.ProductInventoryCheckBatchApplication -Dexec.args=--batch.jobName=productInventoryCheck
)

exit /b %ERRORLEVEL%
