export const Cursos = () =>{
    return <section className="w-full">
            <div className="relative w-full justify-evenly space-x-4 flex flex-row p-15">
                <span>
                    <p className="absolute text-white font-bold z-10">Barbería inicial</p>
                    <img className="absolute h-[120px] w-auto brightness-50"
                    src={academia || null}/>                
                    <button>Más información</button>
                </span>    
                <span>
                    <p className="absolute text-white font-bold z-10">Barbería avanzada</p>
                    <img className="absolute h-[120px] w-auto brightness-50"
                    src={academia || null}/>                
                    <button>Más información</button>
                </span>  
                <span className="absolute">
                    <p className="absolute text-white font-bold z-10">Cursos online</p>
                    <img className="absolute h-[120px] w-auto brightness-50"
                    src={academia || null}/>                
                    <button>Más información</button>
                </span>                          
            </div>
        </section>
}            
