import { Instagram, Mail, Youtube, Radio, MapPin, Phone } from 'lucide-react'

function FindUs(){
    return(
        <section className="w-full mt-12">

            <div className="flex flex-col align-center justify-center text-center space-x-4 mt-2">
                <h4 className="text-white text-3xl md:text-4xl font-bold mb-2">Sucursales</h4>
                <div className="flex flex-wrap space-x-2 justify-around">
                    <span className='flex flex-col'>
                        <a className="font-bold" href="https://maps.app.goo.gl/3uXw44SKcXgg4vN16" target='_blank'>
                        La Plata
                        </a>
                        <small className='flex flex-row align-center justify-center gap-1'>
                            <MapPin size={16}/>
                            6 N° 1080 e/ 54 y 55
                        </small>
                        <iframe 
                            src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d204.47584738514095!2d-57.945579128819624!3d-34.91614621448274!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x95a2e743832e0fe5%3A0x2e870cb0479d9568!2s10%20Peluqueria!5e0!3m2!1ses-419!2sar!4v1764272480330!5m2!1ses-419!2sar" 
                            style={{ border: 0 }}
                            loading='lazy'
                        />
                    </span>
                    <span className='flex flex-col'>
                        <a className="font-bold"href="maps.app.goo.gl/jqq9kqqQCQ5puZCG8" target='_blank'>Ensenada</a>
                        <small className='flex flex-row align-center justify-center gap-1'>
                            <MapPin size={16}/>
                            Marqués de Avilés N° 422 e/ San Martín y Alem
                        </small>
                        <iframe
                          src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d409.2198756478548!2d-57.904714409187086!3d-34.86228231778029!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x95a2e5001a630e17%3A0x15e9be679dbea076!2s10%20Peluquer%C3%ADa%20Ensenada!5e0!3m2!1ses-419!2sar!4v1764272400855!5m2!1ses-419!2sar"
                          style={{ border: 0 }}
                          loading='lazy'
                        />
                    </span>
                </div>
            </div>    

            <div className="flex flex-wrap align-center justify-evenly mt-14">
                <div className="flex flex-col align-center justify-center text-center space-x-4 mt-2">
                    <h4 className="text-white text-3xl md:text-4xl font-bold mb-2">Seguinos</h4>
                    <div className='flex flex-wrap justify-center align-center'>
                        <span className='flex flex-row gap-2'>
                            <a href="https://www.instagram.com/10peluqueria/" target='_blank'>
                                <Instagram/>
                            </a>
                            <a href="https://www.youtube.com/@10peluqueria" target='_blank'>
                                <Youtube/>
                            </a>
                            <a href="https://kick.com/10peluqueria" target='_blank'>
                                <Radio />
                            </a>
                        </span>
                    </div>
                </div>
   
                <div className="flex flex-col align-center justify-center text-center space-x-4 mt-2">
                    <h4 className="text-white text-3xl md:text-4xl font-bold mb-2">Contacto</h4>
                    <div className="flex flex-wrap justify-center align-center">
                        <span className='flex flex-row gap-2'>
                            <a href="#">
                                <Phone/>
                            </a>
                            <a href="#">
                                <Mail/>
                            </a>
                        </span>
                    </div>
                </div>
            </div>
        </section>
    )
}

export default FindUs
