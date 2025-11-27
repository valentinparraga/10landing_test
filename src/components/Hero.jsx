import heroImg from '../assets/sucursal ensenada.jpg';

function Hero() {
  return (
    <div className="relative h-[500px] w-full">
      <img
        className="absolute inset-0 w-full h-full object-cover blur-[1px] brightness-50"
        src={heroImg}
      />

      <div className="absolute inset-0 z-10 flex flex-col items-center justify-center text-center px-4">
        <h2 className="text-white text-3xl md:text-4xl font-bold mb-4">
          "UN LUGAR PARA LOS QUE SE PONEN LA 10"
        </h2>

        <p className="text-white text-sm md:text-base max-w-2xl">
          10 PELUQUERIA nace en 2016, bajo el nombre de <span className='text-shadow-xl'>FA BARBER TEAM</span> en la
          ciudad de Ensenada con Franco Agostinelli como dueño fundador. En base a esfuerzo y
          sacrificio, se logró añadir al equipo de trabajo a los mejores
          barberos de la ciudad.
          <br />
          <span className='font-semibold'>
            Actualmente contamos con sucursales en Ensenada y La Plata.
          </span>  
        </p>
      </div>
    </div>
  );
}

export default Hero;