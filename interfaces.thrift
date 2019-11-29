/**
*  COMMENT SECTION
**/
/* */
enum ElementType{
    CONTROLLER = 1
    CLOUD = 2
    CLIENT = 3
    LOGGER = 4
    SINK = 5
}

enum ElementState{
    WAITING = 11
    RUNNING = 12
    RESET = 13
    STOP = 14
    READY = 15
}

enum ModelState{
    UNSET
    AVAILABLE
    DIRT
}

enum LogType{
    MESSAGE = 0
    PERFORMANCE = 1
    SPECS = 2
}

struct ElementConfiguration{
    1:ElementType type;
    2:optional string ip;
    3:optional i32 port;
    4:optional string id;
    5:optional ElementState state;
}

struct ModelConfiguration{
    1:string model_name;
    2:i16 split_layer;
}

struct Test{
    1:bool is_test;
    2:optional i32 number_of_images;
    3:optional i16 edge_batch_size;
    4:optional i16 cloud_batch_size;
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
    3:ElementType element_type;
    4:string message;
}

struct PerformanceMessage {
    1:double timestamp;
    2:string id;
    3:ElementType element_type;
    4:i16 no_images_predicted;
    5:string list_ids;
    6:double elapsed_time;
    7:string decoded_ids;
    8:list<i16> output_dimension;
}

struct SpecsMessage{
    1:double timestamp;
    2:string id;
    3:ElementType element_type;
    4:string spec;
    5:string value;
}

exception FileNotFound{
    1:string description
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
    bool is_cloud_available()
    ModelConfiguration instantiate_model(1:ModelConfiguration model_configuration)
    ModelState set_model_state(1:ModelState model_state)
    void set_test(1:Test test_configuration)
    Test get_test(1:ElementType element_type)
    void test_completed()
    bool is_test_over()
    void run()
    void reset()
    void stop()
}

service LogInterface{
    void log_message(1:Message log_message)
    void log_performance_message(1:PerformanceMessage message)
    void log_specs_message(1:SpecsMessage message)
    void prepare_log(1:LogType log_type)
    FileChunk get_log_chunk(1:LogType log_type, 2:i64 offset, 3:i32 size) throws (1:FileNotFound message)
}


