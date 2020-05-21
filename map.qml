import QtQuick 2.14
import QtPositioning 5.11
import QtLocation 5.11
import QtDataVisualization 1.2
import QtQuick.Controls 2.14


Rectangle {
    id:rectangle
    width: 640
    height: 480
    Plugin {
        id: osmPlugin
        name: "osm"
    }

    Map {
        id: map
        anchors.fill: parent
        plugin: osmPlugin
        zoomLevel: 1
        minimumTilt: 10
        maximumTilt: 80
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
                        // transform: Rotation {origin.x: 20; origin.y: 20; axis { x: 0; y: 1; z: 0 } angle: -90 }
                        // rotation: 90

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
                                    // parent.color = 'red'
                                    parent.opacity = 1
                                    ToolTip.visible = true
                                }
                                onExited: {
                                    parent.color = model.color_marker
                                    parent.opacity = 0.7
                                    ToolTip.visible = false
                                }
                                onDoubleClicked: {
                                  console.log("Clicked")
                                  markermodel.open_detail(model.name_marker)
                                }

                            }
                }

            }
        }

        Slider {
            objectName: "slider"
            x:  x + 700
            width: 1000
            from: 1
            to: 100
          //  value: 25
            stepSize: 1
            live: true // live update of the value attribute value
            onMoved:  MapWidget.updateDate(value)



            MouseArea {
                ToolTip.text: qsTr("hello there") // shows current value of the slider in the tooltip
                visible: true
            }

        }
    }
}

