service HelloSvc {
    string hello_func(1: string fname, 2: string lname)
}

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
    1:binary arr_bytes;
    2:string data_type;
    3:list<i16> shape;
    4:bool last;
}

service NeuralInterface{
    bool exist_model()
    void set_model(1:ModelConfiguration config)
    ModelConfiguration get_configuration()
    void uninstantiate_model()
    NNLayer make_prediction(1:NNLayer data)
}

service ImageLoader{
    NNLayer getImage()
}
