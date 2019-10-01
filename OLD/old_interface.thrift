service NeuralInterface{
    bool exist_model()
    void set_model(1:ModelConfiguration config)
    ModelConfiguration get_configuration()
    void uninstantiate_model()
    NNLayer make_prediction(1:NNLayer data)
}

service ImageLoaderInterface{
    Image get_image()
}

struct Image{
    1:list<string> id;
    2:binary arr_bytes;
    3:string data_type;
    4:list<i16> shape;
    5:bool last;
}