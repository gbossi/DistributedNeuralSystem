/**
*  COMMENT SECTION
**/
/* */
enum ElementType{
    CONTROLLER
    CLOUD
    CLIENT
    LOGGER
    SINK
}

enum ElementState{
    WAITING
    RUNNING
    RESET
    STOP
}

enum ModelState{
    UNSET
    AVAILABLE
    DIRT
}

struct ElementConfiguration{
    1:ElementType type;
    2:optional string ip;
    3:optional i32 port;
}

struct ModelConfiguration{
    1:string model_name;
    2:i16 split_layer;
}

struct Configuration{
    1:list<ElementConfiguration> elements_configuration
}


struct Image{
    1:list<string> id;
    2:binary arr_bytes;
    3:string data_type;
    4:list<i16> shape;
    5:optional bool last;
}

struct FileChunk {
  1: binary data;
  2: i64 remaining;
}

struct Message {
    1:double timestamp;
    2:string id;
    3:ElementType server_type;
    4:string message;
}

service SinkInterface{
    void put_partial_result(1:Image result)
    Image get_remote_partial_result(1:i16 batch_dimension)
}


service ControllerInterface{
    Configuration get_new_configuration()
    ElementState get_state(1:string element_id)
    ElementState set_state(1:string element_id, 2:ElementState new_state)
    FileChunk get_model_chunk(1:ElementType server_type, 2:i64 offset, 3:i32 size)
    string register_element(1:ElementConfiguration element_configuration)
    bool is_model_available()
}

service MasterInterface{
    bool setModel(1:ModelConfiguration model_configuration)
    bool setModelState(1:ModelState model_state)
    Configuration get_current_configutation()
    bool reset()
    bool stop()
}

service LogInterface{
    void log_message(1:Message log_message)
}

