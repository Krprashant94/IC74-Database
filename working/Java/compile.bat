@echo off
javac -cp .;sqlite-jdbc-3.23.1.jar Android.java
java -cp .;sqlite-jdbc-3.23.1.jar Android
del Android.class
pause