struct NNLayer{
    1:binary arr_bytes;
    2:string data_type;
    3:list<i16> shape;
}

struct ModelConfiguration{
    1:string model_name;
    2:i16 split_layer;
}

struct Image{
    1:list<string> id;
    2:binary arr_bytes;
    3:string data_type;
    4:list<i16> shape;
    5:bool last;
}

service NeuralInterface{
    bool exist_model()
    void set_model(1:ModelConfiguration config)
    ModelConfiguration get_configuration()
    void uninstantiate_model()
    NNLayer make_prediction(1:NNLayer data)
}

service ImageLoader{
    Image get_image()
}

service SinkInterface{
    void put_partial_result(1:Image result)
    Image get_partial_result(1:i16 batch_dimension)
}


