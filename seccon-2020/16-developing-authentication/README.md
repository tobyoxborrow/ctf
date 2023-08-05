# 16 Developing Authentication

Development has pushed their initial authentication page here. I hope it's
secure.

# Design

The challenge provided a link to a login page.

# Write-up

This was a very quick one...

Go to the link provided. Right-click -> view source:

```HTML
<link rel="stylesheet" href="/static/style.css" type="text/css">
<!-- Remember to remove the testing username/password: devuser/&JPGX&4&goYDtwqL&tQH -->

<form action="/login" method="POST">
<div class="login">
<div class="login-screen">
<div class="app-title">
<h1>Login</h1>
</div>
<div class="login-form">
<div class="control-group">
				<input type="text" class="login-field" value="" placeholder="username" name="username">
<label class="login-field-icon fui-user" for="login-name"></label></div>
<div class="control-group">
				<input type="password" class="login-field" value="" placeholder="password" name="password">
<label class="login-field-icon fui-lock" for="login-pass"></label></div>
<input type="submit" value="Log in" class="btn btn-primary btn-large btn-block">

</div>
</div>
</div>
</form>
```

At the top is a comment with credentials username devuser password &JPGX&4&goYDtwqL&tQH.

Login with the credentials in the HTML source code and the flag is displayed on
the next page.
