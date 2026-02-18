@echo off
cd /d "C:\Users\SUNIL\OneDrive\Desktop\voice-assisstant ai"
echo hello> demo_input.txt
echo how are you>> demo_input.txt
echo exit>> demo_input.txt
type demo_input.txt | "C:\Users\SUNIL\AppData\Local\Programs\Python\Python314\python.exe" app.py
del demo_input.txt
pause
