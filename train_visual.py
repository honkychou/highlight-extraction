from Visual.nets import get_vis_model
from Gen.visual_gen import data_gen
from tensorflow.keras.callbacks import ModelCheckpoint,EarlyStopping
from tensorflow.keras.models import load_model
from tensorflow.keras import losses,optimizers
from tensorflow.keras import backend as K 
import pickle

def training_SlowFast(opt_type='sgd',steps=100,epochs=10,batch_size=1,depth='v1'):
    K.clear_session()
    model = get_vis_model(depth)
    opt = None
    if opt_type == 'rms':
        #opt= optimizers.RMSprop(lr=1e-3, rho=0.9, epsilon=1e-8)
        opt= optimizers.Nadam(lr=0.002, beta_1=0.9, beta_2=0.999, epsilon=None, schedule_decay=0.004)
    else:
        opt = optimizers.SGD(lr=1e-5)
    if batch_size > 1:
        model.compile(loss=losses.binary_crossentropy, optimizer=opt, metrics = ['acc'])
    else:
        model.compile(loss=losses.binary_crossentropy, optimizer=opt, metrics = ['acc'])
    
    try:
        model.load_weights("{}-weights-{}.h5".format('Visual',depth), by_name=True)
        pass
    except:
        print('not load')
        pass

    filepath="{}-weights-{}.h5".format('Visual',depth)
    es = EarlyStopping(monitor='val_loss', mode='min', verbose=0,patience=5)
    ck = ModelCheckpoint(filepath, monitor='val_loss', verbose=1, save_best_only=True, mode='min')
    history=model.fit_generator(data_gen('train',batch_size),steps_per_epoch=steps , epochs=epochs, validation_data=data_gen('val',2), validation_steps=200,callbacks=[ck,es],verbose=1)
    with open('visual_{}.pkl'.format(depth),'wb') as fp:
        pickle.dump(history.history, fp)
    del model

if __name__ == '__main__':
    training_SlowFast(opt_type='sgd',steps=1000,epochs=20,batch_size=4,depth='v1')