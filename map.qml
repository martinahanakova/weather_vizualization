import QtQuick 2.11
import QtPositioning 5.11
import QtLocation 5.11

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
        MapRectangle {
            color: 'green'
            rotation: 90
            z: 90
            opacity: 0.5
                border.width: 2
                topLeft {
                    latitude: 44
                    longitude: -93
                    altitude: 2000
                }
                bottomRight {
                    latitude: 42
                    longitude: -91
                    altitude: 0
                }
         }
        MapItemView{
            model: markermodel
            delegate: MapQuickItem {
                coordinate: model.position_marker
                anchorPoint.x: image.width
                anchorPoint.y: image.height
                sourceItem:
                    Image { id: image; source: model.source_marker }
            }
        }
    }
}

