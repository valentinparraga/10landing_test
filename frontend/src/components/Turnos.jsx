export default function Turnos (){

    const barberos = [
        {id:1 ,name: "Franco Agostinelli"},
        {id:2 ,name: "Juan Varas"},
        {id:3 ,name: "Luca Rosales"},
        {id:4 ,name: "Emanuel Siman"},
        {id:5 ,name: "Roman Ortiz"},
    ]

    return <section
            id="turnos"
            className="w-full">

        <h2 className="font-bold">Agendá tu turno:</h2>

        <div className="w-full px-2 py-4">
            <h3 className="font-bold text-2xl">Sucursal</h3>
            <div className="flex flex-wrap align-center justify-center gap-1">
                <button>Ensenada</button>
                <button>La Plata</button>
            </div>
        </div>

        <div className="w-full px-2 py-4">
            <h3 className="font-bold text-2xl">Servicio</h3>
            <div className="flex flex-wrap align-center justify-center gap-1">
                <button>Corte</button>
                <button>Barba</button>
                <button>Corte + barba</button>                
                <button>Color: mechas</button>
                <button>Color: global</button>
            </div>
        </div>

        <div className="w-full px-2 py-4">
            <h3 className="font-bold text-2xl">Barbero</h3>
            <div className="flex flex-wrap align-center justify-center gap-1">
                {barberos.map(barb =>(
                    <button key={barb.id}>{barb.name}</button>
                ))}
            </div>
        </div>

        <button>Confirmar</button>
    </section>
}