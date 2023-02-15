export default {
    "Task": {
        "Id": true,
        "id": true,
        "title": true,
        "description": true,
        "status": true
    },
    "TaskConnection": {
        "pageInfo": "PageInfo",
        "edges": "TaskEdge"
    },
    "PageInfo": {
        "length": true,
        "pages": true,
        "extra": true
    },
    "TaskEdge": {
        "node": "Task",
        "cursor": true
    },
    "Error": {
        "messages": "ErrorMessage",
        "meta": true,
        "error": true
    },
    "ErrorMessage": {
        "field": true,
        "type": true,
        "text": true
    },
    "Deleted": {
        "count": true
    }
}