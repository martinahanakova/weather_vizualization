import QtQuick 2.14
import QtQuick.Window 2.14
import QtQuick3D 1.14

Item {

    Rectangle {
        id: qt_logo
        width: 230
        height: 230
        anchors.top: parent.top
        anchors.left: parent.left
        anchors.margins: 10
        color: "transparent"

        layer.enabled: true

        Rectangle {
            anchors.fill: parent
            color: "black"

            Image {
                anchors.fill: parent
                source: "qt_logo.png"
            }
            Text {
                id: text5
                anchors.bottom: parent.bottom
                anchors.left: parent.left
                color: "white"
                font.pixelSize: 17
                text: qsTr("The Future is Written with Qt")
            }

            transform: Rotation {
                id: rotation
                origin.x: qt_logo.width / 2
                origin.y: qt_logo.height / 2
                axis { x: 1; y: 0; z: 0 }
            }

            PropertyAnimation {
                id: flip1
                target: rotation
                property: "angle"
                duration: 600
                to: 180
                from: 0
            }
            PropertyAnimation {
                id: flip2
                target: rotation
                property: "angle"
                duration: 600
                to: 360
                from: 180
            }
        }
    }

    View3D {
        id: view
        anchors.fill: parent
        camera: camera
        renderMode: View3D.Overlay

        PerspectiveCamera {
            id: camera
            position: Qt.vector3d(0, 200, -300)
            rotation: Qt.vector3d(30, 0, 0)
        }

        DirectionalLight {
            rotation: Qt.vector3d(30, 0, 0)
        }

        Model {
            id: cube
            visible: true
            position: Qt.vector3d(0, 0, 0)
            source: "#Cube"
            materials: [ DefaultMaterial {
                    diffuseMap: Texture {
                        id: texture
                        sourceItem: qt_logo
                        flipV: true
                    }
                }
            ]
            rotation: Qt.vector3d(0, 90, 0)

            SequentialAnimation on rotation {
                loops: Animation.Infinite
                PropertyAnimation {
                    duration: 5000
                    to: Qt.vector3d(360, 0, 360)
                    from: Qt.vector3d(0, 0, 0)
                }
            }
        }
    }


