import QtQuick 2.11
import QtPositioning 5.11
import QtLocation 5.11
import QtDataVisualization 1.2
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
        zoomLevel: 5
        MapItemView{
            id: mapItemView
            model: markermodel
            delegate: MapQuickItem {
                zoomLevel: 6
                coordinate: model.position_marker
                anchorPoint.x: rectangle2.width
                anchorPoint.y: rectangle2.height
               // opacity: 0.7
                sourceItem:
                    // TODO: rotate to create 2.5D view - rotation of the object along with text needs to be adjusted
                    Rectangle {
                        id: rectangle2
                        width: 50
                        height: 100
                       // transform: Rotation {origin.x: 20; origin.y: 20; axis { x: 0; y: 1; z: 0 } angle: -90 }
                      //  rotation: 90

                        color: model.color_marker
                        border.color: "black"
                        border.width: 5
                        radius: 10
                        opacity: 0.7

                        Text {
                            anchors.fill: parent
                            text: model.name_marker +"\n"+ model.value_marker
                            visible: true
                        }

                        MouseArea {
                                anchors.fill: parent
                                hoverEnabled: true
                                cursorShape: Qt.WhatsThisCursor
                                onEntered: {
                                 //   parent.color = 'red'
                                    parent.opacity = 1
                         }
                                onExited: {
                                    parent.color = model.color_marker
                                    parent.opacity = 0.7
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


              /*     Model {
                                    id: image
                                  //  width: 91
                                  //  height: 117
                                    source: "#Sphere"
                                }  */

            }
        }
    }
}
