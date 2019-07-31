import React, { useState } from "react";
import Avatar from "@material-ui/core/Avatar";
import Button from "@material-ui/core/Button";
import CssBaseline from "@material-ui/core/CssBaseline";
import TextField from "@material-ui/core/TextField";
import FormControlLabel from "@material-ui/core/FormControlLabel";
import Checkbox from "@material-ui/core/Checkbox";
import Link from "@material-ui/core/Link";
import Grid from "@material-ui/core/Grid";
import LockOutlinedIcon from "@material-ui/icons/LockOutlined";
import Typography from "@material-ui/core/Typography";
import { makeStyles } from "@material-ui/core/styles";
import Container from "@material-ui/core/Container";
import * as APIUtility from "../../Util/API";
import { Redirect } from "react-router";
import * as actions from "../../Store/Actions/index";
import { connect } from "react-redux";

const useStyles = makeStyles(theme => ({
  "@global": {
    body: {
      backgroundColor: theme.palette.common.white
    }
  },
  paper: {
    marginTop: theme.spacing(8),
    display: "flex",
    flexDirection: "column",
    alignItems: "center"
  },
  avatar: {
    margin: theme.spacing(1),
    backgroundColor: theme.palette.secondary.main
  },
  form: {
    width: "100%", // Fix IE 11 issue.
    marginTop: theme.spacing(1)
  },
  submit: {
    margin: theme.spacing(3, 0, 2)
  }
}));

function SignIn(props) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [redirectBool, setRedirectBool] = useState(false);

  const classes = useStyles();

  const handleUsernameChange = event => {
    setUsername(event.target.value);
  };

  const handlePasswordChange = event => {
    setPassword(event.target.value);
  };

  function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  const getToken = () => {
    const body = {
      username: username,
      password: password,
      grant_type: "password",
      client_id: "hHR0XLBuqPSapYTv1H8OvMCq7F7JG1b0JOFdJPKy"
    };
    const headers = new Headers();
    headers.append("Content-Type", "application/json");
    // headers.append("Content-Type", "application/x-www-form-urlencoded");

    const options = {
      method: "POST",
      headers: headers,
      body: JSON.stringify(body)
    };

    console.log(options);

    APIUtility.API.makeAPICall(APIUtility.GET_TOKEN, null, options)
      .then(response => response.json())
      .then(async response => {
        console.log(response);
        props.setToken(response.access_token);

        await sleep(2000);
        setRedirectBool(true);
      });
  };

  if (redirectBool === true) {
    return <Redirect to="/" />;
  }

  return (
    <Container component="main" maxWidth="xs">
      <CssBaseline />
      <div className={classes.paper}>
        <Avatar className={classes.avatar}>
          <LockOutlinedIcon />
        </Avatar>
        <Typography component="h1" variant="h5">
          Sign in
        </Typography>
        <form className={classes.form} noValidate>
          <TextField
            variant="outlined"
            margin="normal"
            required
            fullWidth
            id="username"
            label="Username"
            name="username"
            autoComplete="username"
            onChange={handleUsernameChange}
            autoFocus
          />
          <TextField
            variant="outlined"
            margin="normal"
            required
            fullWidth
            name="password"
            label="Password"
            type="password"
            id="password"
            autoComplete="current-password"
            onChange={handlePasswordChange}
          />
          <FormControlLabel control={<Checkbox value="remember" color="primary" />} label="Remember me" />
          <Button onClick={getToken} fullWidth variant="contained" color="primary" className={classes.submit}>
            Sign In
          </Button>
          <Grid container>
            <Grid item xs>
              <Link href="#" variant="body2">
                Forgot password?
              </Link>
            </Grid>
            <Grid item>
              <Link href="#" variant="body2">
                {"Don't have an account? Sign Up"}
              </Link>
            </Grid>
          </Grid>
        </form>
      </div>
    </Container>
  );
}

const mapDispatchToProps = dispatch => {
  return {
    setToken: token => dispatch(actions.setToken(token))
  };
};

export default connect(
  null,
  mapDispatchToProps
)(SignIn);
