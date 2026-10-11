/**
 * Kitchen Alert: the parts of the player that differ from Space Alert.
 * Loaded after player.js by kitchen-player.htm, and overrides events and widgets by name.
 * The audio elements keep the Space Alert ids (alert, incoming_data, ...) but point to
 * the Kitchen Alert recordings in kitchenalert/audio/, so the AudioManager works unchanged.
 *
 * This program is free software: you can redistribute it and/or modify it under the
 * terms of the GNU General Public License as published by the Free Software Foundation,
 * either version 3 of the License, or (at your option) any later version.
 */

var KA_COLOR = "#ff9a3c";
var KA_DIM = "rgba(255,154,60,0.25)";
var SIDE_COLORS = {"red": "#e5383b", "blue": "#3a86ff"};

//========//
// Events //
//========//

function Order(start, turn, large, room) {
    this.start = start;
    this.turn = turn;
    this.large = large;
    this.room = room;
    this.end = start + 15;
    this.text = large ? "Large Order" : "New Order";
    this.widgetType = OrderWidget;
    var parts = ["time" + turn.toString(), large ? "large_order" : "order", "room_" + room];
    this.tracks = ["alert"].concat(parts, ["repeat"], parts);
    this.message = timeString(start) + " - Time T+" + turn.toString() + " "
                 + (large ? "Large order" : "New order") + ", " + capitalize(room) + " dining room";
}

function IncomingData(start) {
    this.start = start;
    this.end = start + 5;
    this.text = "Delivery";
    this.widgetType = IncomingDataWidget;
    this.tracks = ["incoming_data"];
    this.message = timeString(start) + " - Delivery (each player may draw one card)";
}

function DataTransfer(start) {
    this.start = start;
    this.end = start + 13;
    this.text = "Handover";
    this.widgetType = DataTransferWidget;
    this.tracks = ["data_transfer"];
    this.message = timeString(start) + " - Handover (each player may give one card to another player)";
}

function CommunicationsDown(start, length) {
    this.start = start;
    if (length < 5)
        length = 5;
    this.end = start + length + 2;
    this.text = "Rush Hour";
    this.widgetType = RushWidget;
    this.tracks = ["comm_down", "noise" + (length - 3).toString(), "comm_restored"];
    this.message = timeString(start) + " - Rush hour, no talking (" + length.toString() + " seconds)";
}

function PhaseEvent(start, phase, remaining, lastPhase) {
    this.start = start;
    this.phase = phase;
    this.text = '';
    this.remaining = remaining;
    this.lastPhase = (typeof(lastPhase) === 'undefined') ? this.phase == 3 : lastPhase;
    var length = remaining == 7 ? (this.lastPhase ? 14 : 13) : 5;
    this.phaseEnd = this.start + this.remaining;
    this.end = start + length;
    this.widgetType = PhaseEventWidget;
    this.tracks = ["phase" + phase.toString() + "_" + remaining.toString()];
    if (remaining == 7)
        this.message = timeString(start + 7) + " - "
                     + (this.lastPhase ? "Kitchen closes" : "Phase " + phase.toString() + " ends");
    else this.message = null;
}

//=========//
// Widgets //
//=========//

Label.draw = function() {
    var labels = Label.stack.call(this);
    var first = labels[0].rect, last = labels[labels.length-1].rect;
    ctx.save();
    ctx.clearRect(first.x, first.y, first.width, last.y + last.height + Label.descent - first.y);
    ctx.font = Label.font;
    ctx.textAlign = "center";
    ctx.fillStyle = KA_COLOR;
    for (var i = 0; i < labels.length; i++)
        ctx.fillText(labels[i].text, labels[i].rect.x + labels[i].rect.width/2,
                     labels[i].rect.y + Label.baseline);
    ctx.restore();
}

// Between announcements: a plate with a timer hand going round.
Radar.init = function() {
    this.frame = 0;
    this.interval = 50;
    this.frameCount = 72;
    this.radius = 200;
    var r = this.radius + 10;
    this.rect = new Rectangle(animator.center.x-r, animator.center.y-r, 2*r, 2*r);
}

Radar.draw = function() {
    if (!this.running)
        return;
    var pos = this.frame/this.frameCount * 2*Math.PI - 0.5*Math.PI;
    ctx.save();
    ctx.clearRect(this.rect.x, this.rect.y, this.rect.width, this.rect.height);
    ctx.translate(animator.center.x, animator.center.y);
    ctx.strokeStyle = KA_COLOR;
    ctx.lineWidth = 5;
    ctx.beginPath(); ctx.arc(0, 0, this.radius, 0, 2*Math.PI); ctx.stroke();
    ctx.lineWidth = 2;
    ctx.beginPath(); ctx.arc(0, 0, this.radius * 0.72, 0, 2*Math.PI); ctx.stroke();
    ctx.fillStyle = KA_DIM;
    ctx.beginPath(); ctx.moveTo(0, 0); ctx.arc(0, 0, this.radius * 0.72, pos - Math.PI/8, pos); ctx.closePath(); ctx.fill();
    ctx.lineWidth = 5;
    ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(this.radius * 0.72 * Math.cos(pos), this.radius * 0.72 * Math.sin(pos)); ctx.stroke();
    ctx.restore();
}

function drawPlate(x, y, r, color) {
    ctx.strokeStyle = color;
    ctx.lineWidth = 4;
    ctx.beginPath(); ctx.arc(x, y, r, 0, 2*Math.PI); ctx.stroke();
    ctx.lineWidth = 2;
    ctx.beginPath(); ctx.arc(x, y, r * 0.62, 0, 2*Math.PI); ctx.stroke();
}

// An order: plates for the size, the floor plan with the guests' dining room lit,
// and the round the order arrives.
var OrderWidget = Object.create(TimerWidget);
OrderWidget.init = function(event) {
    this.interval = 150;
    this.frameCount = 6;
    this.rect = new Rectangle(animator.center.x-330, animator.center.y-110, 660, 220);
    this.order = event;
}

OrderWidget.draw = function() {
    var pulse = (this.frame < this.frameCount / 2 ? this.frame : this.frameCount - this.frame) / (this.frameCount / 2);
    ctx.save();
    ctx.clearRect(this.rect.x, this.rect.y, this.rect.width, this.rect.height);
    ctx.translate(animator.center.x, animator.center.y);

    // size: one plate or two
    if (this.order.large) {
        drawPlate(-255, -30, 34, KA_COLOR);
        drawPlate(-255, 50, 34, KA_COLOR);
    } else drawPlate(-255, 0, 42, KA_COLOR);

    // floor plan as on the board: dining rooms north (red left, blue right), kitchens south
    var w = 110, h = 70, gap = 6;
    var rooms = [["red", -w - gap/2, -h - gap/2], ["blue", gap/2, -h - gap/2],
                 ["kitchen", -w - gap/2, gap/2], ["kitchen", gap/2, gap/2]];
    for (var i = 0; i < rooms.length; i++) {
        var x = rooms[i][1], y = rooms[i][2];
        if (rooms[i][0] == this.order.room) {
            ctx.globalAlpha = 0.45 + 0.55 * (1 - pulse);
            ctx.fillStyle = SIDE_COLORS[this.order.room];
            ctx.fillRect(x, y, w, h);
            ctx.globalAlpha = 1;
        }
        ctx.strokeStyle = rooms[i][0] == "kitchen" ? KA_COLOR : SIDE_COLORS[rooms[i][0]];
        ctx.lineWidth = rooms[i][0] == "kitchen" ? 2 : 4;
        ctx.strokeRect(x, y, w, h);
    }

    // round
    ctx.strokeStyle = KA_COLOR;
    ctx.lineWidth = 4;
    ctx.beginPath(); ctx.arc(255, 0, 52, 0, 2*Math.PI); ctx.stroke();
    ctx.fillStyle = KA_COLOR;
    ctx.font = "30pt Sans-serif";
    ctx.textAlign = "center";
    ctx.fillText("T+" + this.order.turn.toString(), 255, 14);
    ctx.restore();
}

// Rush hour: a crossed-out speech bubble.
var RushWidget = Object.create(TimerWidget);
RushWidget.init = function(event) {
    this.interval = 250;
    this.frameCount = 4;
    // keep clear of the text labels above the widget
    this.rect = new Rectangle(animator.center.x-200, animator.center.y-150, 400, 330);
}

RushWidget.draw = function() {
    ctx.save();
    ctx.clearRect(this.rect.x, this.rect.y, this.rect.width, this.rect.height);
    ctx.translate(animator.center.x, animator.center.y);
    ctx.strokeStyle = this.frame % 2 ? KA_COLOR : "rgba(255,154,60,0.6)";
    ctx.lineWidth = 8;
    ctx.beginPath();
    ctx.ellipse(0, 0, 130, 85, 0, 0, 2*Math.PI);
    ctx.stroke();
    ctx.beginPath(); ctx.moveTo(-55, 76); ctx.lineTo(-90, 135); ctx.lineTo(-10, 83); ctx.stroke();
    ctx.lineWidth = 12;
    ctx.beginPath(); ctx.moveTo(-150, 140); ctx.lineTo(150, -130); ctx.stroke();
    ctx.restore();
}

PhaseEventWidget.draw = function() {
    var text;
    var enlargeLastLine = false;
    if (this.event instanceof StartEvent)
        text = "Doors open\n\nPhase 1";
    else {
        var name = this.event.lastPhase ? "Kitchen" : "Phase " + this.event.phase.toString();
        var ends = this.event.lastPhase ? "\ncloses in" : "\nends in";
        if (this.event.remaining == 7) {
            var remaining = this.event.phaseEnd - animator.seconds;
            if (remaining > 5)
                text = name + ends + "\n\n";
            else if (remaining > 0) {
                text = name + ends + "\n\n" + remaining.toString();
                enlargeLastLine = true;
            }
            else if (this.event.lastPhase)
                text = "Kitchen\nis closed";
            else if (remaining >= -2)
                text = name + "\nhas ended";
            else
                text = "Begin\nPhase " + (this.event.phase + 1).toString();
        }
        else {
            text = name + ends + "\n\n" + (this.event.remaining == 60 ? "1 minute" : "20 seconds");
        }
    }
    ctx.save();
    ctx.fillStyle = KA_COLOR;
    ctx.strokeStyle = KA_COLOR;
    ctx.clearRect(this.rect.x, this.rect.y, this.rect.width, this.rect.height);
    ctx.translate(this.rect.x + this.rect.width/2, this.rect.y + this.rect.height/2);
    ctx.lineWidth = 5;
    ctx.beginPath();
    ctx.arc(0, 0, radius, 0, 2*Math.PI, true);
    ctx.stroke();
    fillWrappedText(text, 50, enlargeLastLine);
    ctx.restore();
}
