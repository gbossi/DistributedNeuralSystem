/**
*  COMMENT SECTION
**/

enum ServerType{
    CLIENT
    LOGGER
    SINK
}

enum ClientState{
    WAITING
    RUNNING
    RESET
}

enum ModelState{
    UNSET
    AVAILABLE
    DIRT
}

struct ServerConfiguration{
    1:ServerType type;
    2:string ip;
    3:i32 port;
}

struct ModelConfiguration{
    1:string model_name;
    2:i16 split_layer;
}

struct Configuration{
    1:ModelConfiguration client_config
    2:list<ServerConfiguration> remote_server_configuration
}


struct Image{
    1:list<string> id;
    2:binary arr_bytes;
    3:string data_type;
    4:list<i16> shape;
    5:bool last;
}

struct FileChunk {
  1: binary data;
  2: i64 remaining;
}


service SinkInterface{
    void put_partial_result(1:Image result)
    Image get_partial_result(1:i16 batch_dimension)
}


service ControllerInterface{
    Configuration get_new_configuration()
    ClientState get_state()
    FileChunk get_model_chunk(1:ServerType server_type, 2:i64 offset, 3:i32 size);
    void register_server(1:ServerConfiguration server_configuration)
}

/*    Configuration get_new_configuration(1:LocalSettings settings) */


service LoggerInterface{
    void log_message(1:string log_message)
}

