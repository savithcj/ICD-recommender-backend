import React, { Component } from "react";

import { Link } from "react-router-dom";
import { makeStyles } from "@material-ui/core/styles";
import AppBar from "@material-ui/core/AppBar";
import Toolbar from "@material-ui/core/Toolbar";
import Typography from "@material-ui/core/Typography";
import IconButton from "@material-ui/core/IconButton";
import MenuIcon from "@material-ui/icons/Menu";
import MenuItem from "@material-ui/core/MenuItem";
import { Menu } from "@material-ui/core";
import { ReactComponent as CheckIcon } from "./icons/round-done-24px.svg";

const useStyles = makeStyles(theme => ({
  root: {
    flexGrow: 1
  },
  menuButton: {
    marginRight: theme.spacing(2)
  },
  title: {
    flexGrow: 1
  }
}));

function ButtonAppBar(props) {
  const classes = useStyles();
  const [anchorEl, setAnchorEl] = React.useState(null);
  const isMenuOpen = Boolean(anchorEl);

  function handleMenuOpen(event) {
    setAnchorEl(event.currentTarget);
  }

  function handleMenuClose(event) {
    setAnchorEl(null);
  }

  function handleToggleLayout(event) {
    props.handleLayoutConfirm();
    setAnchorEl(null);
  }

  function handleResetLayout(event) {
    props.handleResetLayout();
    setAnchorEl(null);
  }

  function handleAdminButton(event) {
    //TODO: Implementation
    console.log("Admin button pressed in menu");
    setAnchorEl(null);
  }

  function handleAboutButton(event) {
    //TODO: Implementation
    console.log("About button pressed in menu");
    setAnchorEl(null);
  }

  const menuId = "settings-menu";

  let renderMenu = props.inModifyMode ? null : (
    //TODO: get rid of class menu item to which is a redirect to the sandbox page
    <Menu
      anchorEl={anchorEl}
      anchorOrigin={{ vertical: "top", horizontal: "right" }}
      id={menuId}
      keepMounted
      transformOrigin={{ vertical: "top", horizontal: "right" }}
      open={isMenuOpen}
      onClose={handleMenuClose}
    >
      <MenuItem component={Link} to={props.firstLinkRoute}>
        {props.firstLinkName}
      </MenuItem>
      <MenuItem onClick={handleToggleLayout}>Customize Layout</MenuItem>
      <MenuItem onClick={handleResetLayout}>Reset Layout</MenuItem>
      <MenuItem onClick={handleAboutButton}>About</MenuItem>
      <MenuItem component={Link} to="/sandbox">
        Sandbox
      </MenuItem>
    </Menu>
  );

  let iconButton = props.inModifyMode ? (
    <IconButton
      edge="end"
      // className={classes.menuButton}
      // aria-label="Settings"
      aria-controls={menuId}
      aria-haspopup="true"
      onClick={props.handleLayoutConfirm}
      color="inherit"
    >
      <CheckIcon />
    </IconButton>
  ) : (
    <IconButton
      edge="end"
      // className={classes.menuButton}
      // aria-label="Settings"
      aria-controls={menuId}
      aria-haspopup="true"
      onClick={handleMenuOpen}
      color="inherit"
    >
      <MenuIcon />
    </IconButton>
  );

  return (
    <div className={classes.root}>
      <AppBar position="static">
        <Toolbar>
          <IconButton edge="start" className={classes.menuButton} color="inherit" aria-label="Menu" />
          <Typography variant="h6" className={classes.title}>
            {props.title}
          </Typography>
          {iconButton}
        </Toolbar>
      </AppBar>
      {renderMenu}
    </div>
  );
}

export default ButtonAppBar;
