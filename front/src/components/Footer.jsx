function Footer(){
    return(
        <footer className="w-full flex flex-col pt-2 bg-neutral-950 mt-20">
            <small>Formación profesional de barberos en habla hispana. Entrenamientos reales. Resultados reales.</small>
            <span className="w-full flex flex-wrap justify-evenly space-x-2 p-5">
                    <a className="text-slate-300" href="#">Terminos y condiciones</a>
                    <a className="text-slate-300" href="#">Trabajá con nosotros</a>
                    <a className="text-slate-300" href="#">Política de privacidad</a>
                    <a className="text-slate-300" href="#">Soporte y ayuda</a>
            </span>
            <p className="font-semibold flex flex-col">
                10peluqueria. Todos los derechos reservados.
            </p>
        </footer>
    )
}

export default Footer
