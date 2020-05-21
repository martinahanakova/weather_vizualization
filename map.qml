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

                sourceItem:
                    Rectangle {
                        id: rectangle2
                        width: 50
                        height: 100

                        color: model.color_marker
                        border.color: "black"
                        border.width: 5
                        radius: 10
                        opacity: 0.7

                        Text {
                            anchors.bottom: parent.top
                            text: model.name_marker +"\n"+ model.value_marker
                            visible: true
                        }

                        MouseArea {
                                id: ma
                                anchors.fill: parent
                                hoverEnabled: true
                                cursorShape: Qt.WhatsThisCursor

                                ToolTip.text: qsTr("Double-click to open detail window")

                                onEntered: {
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
            stepSize: 1
            live: true
            onMoved:  MapWidget.updateDate(value)

            MouseArea {
                ToolTip.text: qsTr("hello there") // shows current value of the slider in the tooltip
                visible: true
            }

        }
    }
}

