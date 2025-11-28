import academia from '../assets/academia.jpg';
import { Barberos } from './Barberos';

function Main(){
    return(
        <div className="w-full flex-col mt-20">
            <span className="mb-1">
                <h3 className="text-2xl md:text-3xl font-bold">BARBEROS</h3>
                <small className='font-semibold'>Contamos con un amplio equipo de barberos dispuestos para ofrecerte el mejor servicio!</small>
            </span>

            <Barberos/>

        </div>
    )
}

export default Main