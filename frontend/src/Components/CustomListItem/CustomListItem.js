import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import List from "@material-ui/core/List";
import ListItem from "@material-ui/core/ListItem";
import ListItemText from "@material-ui/core/ListItemText";
import ListSubheader from "@material-ui/core/ListSubheader";
import IconButton from "@material-ui/core/IconButton";
import ExploreIcon from "@material-ui/icons/ExploreOutlined";
import CheckIcon from "@material-ui/icons/CheckCircleOutlined";
import RejectIcon from "@material-ui/icons/HighlightOff";

const useStyles = makeStyles(theme => ({
  root: {
    flexGrow: 1,
    maxWidth: "100%"
  },
  demo: {
    backgroundColor: theme.palette.background.paper
  },
  title: {
    margin: theme.spacing(4, 0, 2)
  }
}));

function CustomListItem() {
  const classes = useStyles();

  const code = "Y830";
  const description =
    "Surgical operation with transplant of whole organ or tissue as the cause of abnormal reaction or later complication, without mention of misadventure at the time of the procedure";

  return (
    <div className={classes.root}>
      <List
        dense={true}
        subheader={
          <ListSubheader disableSticky={true} id="nested-list-subheader">
            Recommended Codes
          </ListSubheader>
        }
      >
        <ListItem>
          <IconButton aria-label="Explore" title="Explore on Tree">
            <ExploreIcon />
          </IconButton>
          <ListItemText primary={code} secondary={description} />
          <IconButton edge="end" aria-label="Accept" title="Accept">
            <CheckIcon />
          </IconButton>
          <IconButton edge="end" aria-label="Reject" title="Reject">
            <RejectIcon />
          </IconButton>
        </ListItem>
      </List>
    </div>
  );
}

export default CustomListItem;
