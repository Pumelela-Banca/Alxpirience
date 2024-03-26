from flask import Flask, render_template, url_for, flash, redirect
from home.log_in import RegisterForm, LoginForm

app = Flask(__name__)

