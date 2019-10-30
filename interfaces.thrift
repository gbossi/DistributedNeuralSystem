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
    1:optional string id;
    2:ElementType type;
    3:optional string ip;
    4:optional i32 port;
}

struct ModelConfiguration{
    1:string model_name;
    2:i16 split_layer;
}

struct Test{
    1:bool test;
    2:i32 repetition;
    3:optional i32 number_of_images;
    4:optional i16 edge_batch_size;
    5:optional i16 cloud_batch_size;
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
    Configuration get_servers_configuration()
    Configuration get_complete_configuration()
    ElementState get_state(1:string element_id)
    ElementState set_state(1:string element_id, 2:ElementState new_state)
    FileChunk get_model_chunk(1:ElementType server_type, 2:i64 offset, 3:i32 size)
    string register_element(1:ElementConfiguration element_configuration)
    bool is_model_available()
    ModelConfiguration instantiate_model(1:ModelConfiguration model_configuration)
    ModelState set_model_state(1:ModelState model_state)
    void set_test(1:Test test_configuration)
    void reset()
    void stop()
}

service LogInterface{
    void log_message(1:Message log_message)
}

