import React, { Component } from "react";
import * as d3 from "d3";
import { sliderBottom } from "d3-simple-slider";
import ReactDOM from "react-dom";

import APIClass from "../../Assets/Util/API";

class ChordDiagram extends Component {
  constructor(props) {
    super(props);
    this.sliderMin = 1;
    this.sliderMax = 35;
    this.numTicks = 10;
    this.fontType = "sans-serif";
    this.textColor = "black";
    this.defaultSliderValue = 1;
    this.chordClass = "chordVis" + this.props.id;
  }

  componentDidMount() {
    this.getDataFromAPI().then(() => {
      this.drawChordDiagram();
    });
  }

  handleResize() {
    if (this.data === undefined) {
      // console.log("No data");
    } else {
      this.recalculateSizes();
      this.drawChordDiagram();
    }
  }

  recalculateSizes() {
    let elem = ReactDOM.findDOMNode(this).parentNode;
    this.width = elem.offsetWidth;
    this.height = elem.offsetHeight;
    const minSize = Math.min(this.width, this.height);
    this.cRadius = minSize / 3.5;
    this.textSize = minSize / 45;
    this.barHeight = 0.08 * minSize;
    this.centerX = this.width * 0.4;
    this.centerY = this.height / 2;
  }

  addInfoText() {
    let infoG = this.svg.append("g").attr("class", "infoG");
    this.infoText = infoG
      .append("text")
      .attr("y", this.height * 0.05)
      .attr("x", this.width * 0.02)
      .attr("font-family", this.fontType)
      .attr("font-size", this.textSize)
      .attr("fill", this.textColor)
      .text("")
      .style("text-anchor", "left");
  }

  drawChordDiagram() {
    this.recalculateSizes();

    d3.select("div." + this.chordClass)
      .select("svg")
      .remove();

    this.svg = d3
      .select("div." + this.chordClass)
      .append("svg")
      .attr("width", this.width)
      .attr("height", this.height);

    this.addInfoText();

    this.colours = d3
      .scaleLinear()
      .domain(d3.ticks(0, this.parentNames.length, 11))
      .range([
        "#5E4FA2",
        "#3288BD",
        "#66C2A5",
        "#ABDDA4",
        "#E6F598",
        "#f4e542",
        "#FEE08B",
        "#FDAE61",
        "#F46D43",
        "#D53E4F",
        "#9E0142"
      ]);
    this.arcThickness = this.width / 1000;
    this.numPSelections = this.parentSelections.reduce((a, b) => a + b, 0);
    this.selectedParents = [];
    for (let i = 0; i < this.parentSelections.length; i++) {
      if (this.parentSelections[i]) {
        this.selectedParents.push(i);
      }
    }
    this.numBars = 0;
    for (let i = 0; i < this.numPSelections; i++) {
      const selectedParentIndex = this.selectedParents[i];
      const startIndex = this.pData[selectedParentIndex].startIndex;
      const endIndex = this.pData[selectedParentIndex].endIndex;
      for (let j = startIndex; j <= endIndex; j++) {
        this.numBars++;
      }
    }
    if (this.numPSelections !== 0) {
      this.drawBars();
      this.drawSlider();
      this.generateCurves();
    }

    this.drawLegend();

    // rectangle to make it so cursor isn't shown when hovering over ticks
    this.svg
      .append("rect")
      .attr("x", 0)
      .attr("y", this.height * 0.95)
      .attr("width", this.width)
      .attr("height", this.height * 0.05)
      .style("fill-opacity", 1e-6);
  }

  drawBars() {
    //Determine max coded from selected chapters
    this.maxCoded = 0;
    for (let i = 0; i < this.numPSelections; i++) {
      const selectedParentIndex = this.selectedParents[i];
      const startIndex = this.pData[selectedParentIndex].startIndex;
      const endIndex = this.pData[selectedParentIndex].endIndex;
      for (let j = startIndex; j <= endIndex; j++) {
        if (this.data[j].times_coded > this.maxCoded) {
          this.maxCoded = this.data[j].times_coded;
        }
      }
    }

    this.barWidth = 2 * this.cRadius * Math.sin(Math.PI / this.numBars);
    this.bars = [];
    this.sliceAngle = 360 / this.numBars;
    let barCount = 0;
    for (let i = 0; i < this.numPSelections; i++) {
      const selectedParentIndex = this.selectedParents[i];
      const startIndex = this.pData[selectedParentIndex].startIndex;
      const endIndex = this.pData[selectedParentIndex].endIndex;
      for (let j = startIndex; j <= endIndex; j++) {
        let angle = (((barCount * 360) / this.numBars - 90) * Math.PI) / 180;
        let nextAngle;
        if (barCount !== this.numBars - 1) {
          nextAngle = ((((i + 1) * 360) / this.numBars - 90) * Math.PI) / 180;
        } else {
          nextAngle = Math.PI / -2;
        }
        this.bars.push({
          x: this.cRadius * Math.cos(angle) + this.centerX,
          y: this.cRadius * Math.sin(angle) + this.centerY,
          nextX: this.cRadius * Math.cos(nextAngle) + this.centerX,
          nextY: this.cRadius * Math.sin(nextAngle) + this.centerX,
          block: this.data[j].block,
          normTimes: this.data[j].times_coded / this.maxCoded,
          parent: this.data[j].parent,
          description: this.data[j].description,
          angle: angle
        });
        barCount++;
      }
    }

    this.svg
      .selectAll("rect.barRect")
      .data(this.bars)
      .enter()
      .append("rect")
      .attr("x", d => d.x)
      .attr("y", d => d.y)
      .attr("fill", d => this.calcColour(d.parent))
      .attr("class", "barRect")
      .attr("width", d => {
        return this.barHeight * d.normTimes;
      })
      .attr("height", this.barWidth)
      .attr("transform", d => {
        let angle = (d.angle * 180) / Math.PI + this.sliceAngle / 2;
        return "rotate(" + angle + "," + d.x + "," + d.y + ")";
      });

    this.svg
      .selectAll("rect.invisibleRect")
      .data(this.bars)
      .enter()
      .append("rect")
      .attr("x", d => d.x)
      .attr("y", d => d.y)
      .attr("class", "invisibleRect")
      .attr("width", this.barHeight)
      .style("fill-opacity", 1e-6)
      .style("stroke", "black")
      .style("stroke-opacity", 1e-6)
      .attr("height", this.barWidth)
      .attr("id", (d, i) => {
        return "rect" + i;
      })
      .attr("transform", d => {
        let angle = (d.angle * 180) / Math.PI + this.sliceAngle / 2;
        return "rotate(" + angle + "," + d.x + "," + d.y + ")";
      })
      .on("mouseover", (d, i) => {
        this.infoText.text(d.block + ":" + d.description);
        this.drawOverlayCurves(i);
        this.svg.select("#rect" + i).style("stroke-opacity", 1);
      })
      .on("mouseout", (d, i) => {
        this.infoText.text("");
        this.deleteOverlayCurves(i);
        this.svg.select("#rect" + i).style("stroke-opacity", 1e-6);
      });
  }

  generateCurves() {
    this.svg.selectAll("path.curve").remove();

    //generate startpoints and endpoints for the rule curves
    //start points are a little offset from the endpoints
    this.startPoints = [];
    this.endPoints = [];
    this.curveData = [];
    let barCount = 0;
    for (let i = 0; i < this.numPSelections; i++) {
      const selectedParentIndex = this.selectedParents[i];
      const startIndex = this.pData[selectedParentIndex].startIndex;
      const endIndex = this.pData[selectedParentIndex].endIndex;
      for (let j = startIndex; j <= endIndex; j++) {
        let angle = (((barCount * 360) / this.numBars - 90) * Math.PI) / 180;
        let offset = ((360 / this.numBars) * Math.PI) / 180 / 3;
        this.startPoints.push({
          x: this.cRadius * Math.cos(angle + offset) + this.centerX,
          y: this.cRadius * Math.sin(angle + offset) + this.centerY,
          parent: this.data[barCount].parent
        });
        this.endPoints.push({
          x: this.cRadius * Math.cos(angle + 2 * offset) + this.centerX,
          y: this.cRadius * Math.sin(angle + 2 * offset) + this.centerY
        });
        this.curveData.push({
          destinationCounts: this.data[j].destination_counts.split(",").map(Number),
          parentIndex: selectedParentIndex
        });
        barCount++;
      }
    }
    //draw rule curves

    for (let i = 0; i < this.curveData.length; i++) {
      this.drawCurves(i, "", this.arcThickness);
    }
  }

  drawCurves(row, className, strokeWidth) {
    const cData = this.curveData[row];
    const destinationCounts = cData.destinationCounts;
    let col = 0;
    for (let i = 0; i < this.numPSelections; i++) {
      const selectedParentIndex = this.selectedParents[i];
      const startIndex = this.pData[selectedParentIndex].startIndex;
      const endIndex = this.pData[selectedParentIndex].endIndex;
      for (let j = startIndex; j <= endIndex; j++) {
        if (destinationCounts[j] > this.minRules) {
          let bezierString =
            "M" +
            this.startPoints[row].x +
            "," +
            this.startPoints[row].y +
            " Q" +
            this.centerX +
            "," +
            this.centerY +
            " " +
            this.endPoints[col].x +
            "," +
            this.endPoints[col].y;
          this.svg
            .append("svg:path")
            .attr("class", "curve" + className)
            .attr("d", bezierString)
            .style("stroke", this.calcColour(this.parentNames[cData.parentIndex]))
            .attr("stroke-width", strokeWidth)
            .attr("fill", "none");
        }
        col++;
      }
    }
  }

  drawSlider() {
    //this is the cutoff for the minimum number of rules
    this.minRules = 1;
    var slider = sliderBottom()
      .min(this.sliderMin)
      .max(this.sliderMax)
      .width(1.5 * this.cRadius)
      .ticks(this.numTicks)
      .default(this.defaultSliderValue)
      .step(1)
      .on("onchange", val => {
        this.minRules = val;
        this.generateCurves();
      });

    this.svg
      .append("g")
      .attr(
        "transform",
        "translate(" +
          (this.centerX - 0.5 * this.cRadius) +
          "," +
          (this.centerY + this.cRadius + 1.2 * this.barHeight) +
          ")"
      )
      .call(slider);

    this.svg
      .append("text")
      .text("Minimum rules:")
      .attr("font-family", this.fontType)
      .attr("font-size", this.textSize)
      .attr("fill", this.textColor)
      .attr("y", this.centerY + this.cRadius + 1.2 * this.barHeight)
      .attr("x", this.centerX - 0.5 * this.cRadius - 0.02 * this.width)
      .attr("class", "minRuleText")
      .style("text-anchor", "end");
  }

  drawLegend() {
    let sortedPNames = [...this.parentNames];
    let sortedPDescriptions = [...this.parentDescriptions];
    sortedPNames.sort();
    sortedPDescriptions.sort();

    for (let i = 0; i < sortedPNames.length; i++) {
      let g = this.svg
        .append("g")
        .on("mouseover", () => {
          this.infoText.text(sortedPDescriptions[i]);
        })
        .on("mouseout", () => {
          this.infoText.text("");
        })
        .on("click", () => {
          this.parentSelections[i] = !this.parentSelections[i];
          this.drawChordDiagram();
        });

      g.append("text")
        .text(sortedPNames[i])
        .attr("font-family", this.fontType)
        .attr("font-size", this.textSize)
        .attr("fill", this.textColor)
        .attr("y", i * this.textSize * 1.5 + (this.centerY - 0.75 * this.textSize * sortedPNames.length))
        .attr("x", this.centerX + this.cRadius + 2.5 * this.barHeight)
        .attr("class", "legendText")
        .style("text-anchor", "end");

      g.append("rect")
        .attr("fill", this.calcColour(sortedPNames[i]))
        .attr(
          "y",
          i * this.textSize * 1.5 + (this.centerY - 0.75 * this.textSize * sortedPNames.length - 0.01 * this.height)
        )
        .attr("x", this.centerX + this.cRadius + 2.5 * this.barHeight + 5)
        .attr("class", "legendRect")
        .attr("width", this.width * 0.05)
        .attr("height", this.height * 0.01);

      g.append("rect")
        .attr("stroke-width", this.width / 500)
        .attr("stroke", "black")
        .attr("fill", "#808080")
        .attr("fill-opacity", 1.0 * this.parentSelections[i])
        .attr(
          "y",
          i * this.textSize * 1.5 + (this.centerY - 0.75 * this.textSize * sortedPNames.length - 0.015 * this.height)
        )
        .attr("x", this.centerX + this.cRadius + 2.5 * this.barHeight + 5 + this.width * 0.06)
        .attr("class", "legendSelectionRect")
        .attr("width", this.width * 0.015)
        .attr("height", this.height * 0.015);

      const gBBox = g.node().getBBox();
      g.append("rect")
        .attr("fill", "#000000")
        .attr("opacity", 1e-6)
        .attr("y", gBBox.y)
        .attr("x", gBBox.x)
        .attr("class", "legendInvisRect")
        .attr("width", gBBox.width)
        .attr("height", gBBox.height);
    }
  }

  drawOverlayCurves(row) {
    this.drawCurves(row, row, this.arcThickness * 6);
  }

  deleteOverlayCurves(row) {
    this.svg.selectAll("path.curve" + row).remove();
  }

  calcColour(parent) {
    return this.colours(this.parentNames.indexOf(parent));
  }

  getDataFromAPI = () => {
    const url = APIClass.getAPIURL("CODE_BLOCK_USAGE") + "?format=json";
    return fetch(url)
      .then(response => response.json())
      .then(parsedJson => {
        this.data = parsedJson;
        this.pData = [];
        this.parentNames = [];
        this.parentDescriptions = [];
        this.parentSelections = [];
        let parentName = "";
        let pIndex = -1;
        for (let i = 0; i < this.data.length; i++) {
          let curElem = this.data[i];
          if (parentName !== curElem.parent) {
            pIndex++;
            parentName = curElem.parent;
            this.parentNames.push(parentName);
            this.parentDescriptions.push(parentName + ": " + curElem.parent_description);
            this.parentSelections.push(true);
            this.pData.push({
              pName: curElem.parent,
              pDesc: curElem.parent_description,
              startIndex: i,
              blocks: [],
              descriptions: [],
              destCounts: []
            });
          }
          this.pData[pIndex]["endIndex"] = i;
          this.pData[pIndex]["destCounts"].push(curElem.destination_counts.split(",").map(Number));
          this.pData[pIndex]["blocks"].push(curElem.block);
          this.pData[pIndex]["descriptions"].push(curElem.description);
        }
        this.pData.sort((a, b) => {
          return ("" + a.pName).localeCompare(b.pName);
        });
        this.numParents = this.pData.length;
      });
  };

  render() {
    return <div id={"chord" + this.props.id} className={this.chordClass} />;
  }
}

export default ChordDiagram;
