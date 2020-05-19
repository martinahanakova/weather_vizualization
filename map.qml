import QtQuick 2.14
import QtPositioning 5.11
import QtLocation 5.11
import QtDataVisualization 1.2
import QtQuick.Controls 2.14


//import QtQuick3D 1.14



/*Rectangle {
    id:rectangle
    width: 640
    height: 480
    Plugin {
        id: osmPlugin
        name: "osm"
    }
    */

Rectangle {
    id:rectangle
    width: 640
    height: 480
    Plugin {
        id: osmPlugin
        name: "osm"
    }

    property variant locationTC: QtPositioning.coordinate(44.951, -93.192)
    Map {
        id: map
        anchors.fill: parent
        plugin: osmPlugin
        center: locationTC
        minimumTilt: 10
        maximumTilt: 80
        zoomLevel: 5
        MapItemView{
            id: mapItemView
            model: markermodel
            delegate: MapQuickItem {
                zoomLevel: 6
                coordinate: model.position_marker
                anchorPoint.x: rectangle2.width/2
                anchorPoint.y: rectangle2.height/2
               // rotation: 14
              //  transform: Rotation { axis { x: 0; y: 0; z: 1 } angle: 60 }

                sourceItem:
                    // TODO: rotate to create 2.5D view - rotation of the object along with text needs to be adjusted

                    Rectangle {
                        id: rectangle2
                        width: 50
                        height: 100
                     //   transformOrigin: Item.Center
                    //    transform: Rotation {origin.x: 20; origin.y: 20; axis { x: 1; y: 0; z: 0 } angle: -80 }
                      //  rotation: 14

                        color: model.color_marker
                        border.color: "black"
                        border.width: 5
                        radius: 10
                        opacity: 0.7


                        Text {
                            anchors.bottom: parent.top
                            text: model.name_marker +"\n"+ model.value_marker
                         //   font.pixelSize: this.font.pixelSize * 2
                            visible: true
                        }

                        MouseArea {
                                id: ma
                                anchors.fill: parent
                                hoverEnabled: true
                                cursorShape: Qt.WhatsThisCursor

                                ToolTip.text: qsTr("Double-click to open detail window")

                                onEntered: {
                                 //   parent.color = 'red'
                                    parent.opacity = 1
                                    ToolTip.visible = true
                         }
                                onExited: {
                                    parent.color = model.color_marker
                                    parent.opacity = 0.7
                                    ToolTip.visible = false
                                }
                                /*
                                TODO: on clicked - duplicate the view somewhere (top part of screen or window)
                                - needed for scenario of comparison of two different cities
                                - user will be able to open multiple cities views at same time and compare them

                                TODO: on double clicked - open Maťuška´s detail window for the city
                                - trigger either here or in map_widget by a function connected to a button
                                */
                            }
                }

            }
        }

        RangeSlider {
            x:  x + 700
            width: 1000
            from: 1
            to: 100
            first.value: 25
            second.value: 75
            hoverEnabled: true

            MouseArea {
            //    anchors.fill: parent  - blocks slider functionality
                ToolTip.text: qsTr("Slide to define time interval for shown values")
                onEntered: {
                //    ToolTip.visible = true
                }
                onExited: {
                //    ToolTip.visible = false
                }

            }
        }
    }
}
