#-------------------------------------------------------------
#                   usuarios.py
#-------------------------------------------------------------
sc_index = {
    'tags': ['usuarios.py'],
    'responses': {
        '200': {
            'description': 'Página de inicio renderizada correctamente.'
        }
    }
}

sc_register = {
    'tags': ['usuarios.py'],
    'parameters': [
        {
            'name': 'username',
            'in': 'formData',
            'type': 'string',
            'required': True,
            'description': 'Nombre de usuario'
        },
        {
            'name': 'password',
            'in': 'formData',
            'type': 'string',
            'required': True,
            'description': 'Contraseña'
        },
        {
            'name': 'confirm_password',
            'in': 'formData',
            'type': 'string',
            'required': True,
            'description': 'Confirmar contraseña'
        },
        {
            'name': 'mail',
            'in': 'formData',
            'type': 'string',
            'required': True,
            'description': 'Correo electrónico'
        },
        {
            'name': 'phone',
            'in': 'formData',
            'type': 'string',
            'required': True,
            'description': 'Número de teléfono'
        }
    ],
    'responses': {
        '302': {
            'description': 'Redirección a la página de inicio de sesión.'
        },
        '200': {
            'description': 'Usuario registrado correctamente.'
        },
        '400': {
            'description': 'Error en la validación de los datos del formulario.'
        }
    }
}

sc_login = {
    'tags': ['usuarios.py'],
    'parameters': [
        {
            'name': 'username',
            'in': 'formData',
            'type': 'string',
            'required': True,
            'description': 'Nombre de usuario'
        },
        {
            'name': 'password',
            'in': 'formData',
            'type': 'string',
            'required': True,
            'description': 'Contraseña'
        }
    ],
    'responses': {
        '302': {
            'description': 'Redirección a la página de inicio.'
        },
        '200': {
            'description': 'Sesión iniciada correctamente.'
        },
        '400': {
            'description': 'Error en la validación de los datos del formulario.'
        }
    }
}

sc_inicio = {
    'tags': ['usuarios.py'],
    'responses': {
        '200': {
            'description': 'Página de inicio renderizada correctamente.'
        },
        '302': {
            'description': 'Redirección a la página de inicio de sesión.'
        }
    }
}

sc_logout = {
    'tags': ['usuarios.py'],
    'responses': {
        '302': {
            'description': 'Redirección a la página de inicio de sesión.'
        },
        '200': {
            'description': 'Sesión cerrada correctamente.'
        }
    }
}

sc_forgotPassword = {
    'tags': ['usuarios.py'],
    'parameters': [
        {
            'name': 'username',
            'in': 'formData',
            'type': 'string',
            'required': True,
            'description': 'Nombre de usuario registrado'
        },
        {
            'name': 'mail',
            'in': 'formData',
            'type': 'string',
            'required': True,
            'description': 'Correo electrónico registrado'
        }
    ],
    'responses': {
        '302': {
            'description': 'Redirección a la página de inicio de sesión.'
        },
        '200': {
            'description': 'Correo electrónico enviado correctamente.'
        },
        '400': {
            'description': 'Error en la validación de los datos del formulario.'
        }
    }
}

sc_changePassword = {
    'tags': ['usuarios.py'],
    'parameters': [
        {
            'name': 'new_password',
            'in': 'formData',
            'type': 'string',
            'required': True,
            'description': 'Nueva contraseña'
        },
        {
            'name': 'confirm_password',
            'in': 'formData',
            'type': 'string',
            'required': True,
            'description': 'Confirmación de la nueva contraseña'
        }
    ],
    'responses': {
        '302': {
            'description': 'Redirección a la página de inicio de sesión.'
        },
        '200': {
            'description': 'Contraseña actualizada correctamente.'
        },
        '400': {
            'description': 'Error en la validación de los datos del formulario.'
        }
    }
}

sc_changePasswordMail = {
    'tags': ['usuarios.py'],
    'parameters': [
        {
            'name': 'token',
            'in': 'query',
            'type': 'string',
            'required': True,
            'description': 'Token de recuperación de contraseña'
        },
        {
            'name': 'new_password',
            'in': 'formData',
            'type': 'string',
            'required': True,
            'description': 'Nueva contraseña'
        },
        {
            'name': 'confirm_password',
            'in': 'formData',
            'type': 'string',
            'required': True,
            'description': 'Confirmar nueva contraseña'
        },
        {
            'name': 'username',
            'in': 'formData',
            'type': 'string',
            'required': True,
            'description': 'Nombre de usuario'
        }
    ],
    'responses': {
        '200': {
            'description': 'Contraseña actualizada correctamente.',
        },
        '302': {
            'description': 'Redirección a la página de login.'
        },
        '400': {
            'description': 'Contraseña y confirmación no coinciden.'
        },
        '404': {
            'description': 'No se encontró ningún usuario con el nombre especificado.'
        },
        '500': {
            'description': 'Error interno del servidor.'
        }
    }
}

#-------------------------------------------------------------
#                   principal.py
#-------------------------------------------------------------
sc_sensorTemHum = {
    'tags': ['principal.py'],
    'parameters': [
        {
            'name': 'boton',
            'in': 'formData',
            'type': 'string',
            'required': True,
            'description': 'Valor del botón presionado'
        }
    ],
    'responses': {
        '200': {
            'description': 'Datos renderizados en la plantilla sensorTemHum.html',
            'schema': {
                'type': 'object',
                'properties': {
                    'title': {
                        'type': 'string'
                    },
                    'temperatura': {
                        'type': 'number'
                    },
                    'humedad': {
                        'type': 'number'
                    },
                    'estado': {
                        'type': 'string'
                    },
                    'saltoCalefaccion': {
                        'type': 'string'
                    },
                    'metaCalefaccion': {
                        'type': 'string'
                    },
                    'saltoAire': {
                        'type': 'string'
                    },
                    'metaAire': {
                        'type': 'string'
                    }
                }
            }
        },
        '302': {
            'description': 'Redirección a la página de inicio de sesión'
        }
    }
}

sc_sensorAlarma = {
    'tags': ['principal.py'],
    'parameters': [
        {
            'name': 'boton',
            'in': 'formData',
            'type': 'string',
            'required': True,
            'description': 'Valor del botón presionado'
        }
    ],
    'responses': {
        '200': {
            'description': 'Datos renderizados en la plantilla sensorAlarma.html',
            'schema': {
                'type': 'object',
                'properties': {
                    'title': {
                        'type': 'string'
                    },
                    'estado': {
                        'type': 'string'
                    }
                }
            }
        },
        '302': {
            'description': 'Redirección a la página de inicio de sesión'
        }
    }
}

sc_sensorLuzAutomatica = {
    'tags': ['principal.py'],
    'parameters': [],
    'responses': {
        '200': {
            'description': 'Operación exitosa.',
        },
        '302': {
            'description': 'Redirección a la página de inicio de sesión.',
        },
        '401': {
            'description': 'No autorizado.',
        },
        '500': {
            'description': 'Error interno del servidor.',
        }
    }
}

sc_sensorCO2 = {
    'tags': ['principal.py'],
    'parameters': [],
    'responses': {
        '200': {
            'description': 'Operación exitosa.',
        },
        '302': {
            'description': 'Redirección a la página de inicio de sesión.',
        },
        '401': {
            'description': 'No autorizado.',
        },
        '500': {
            'description': 'Error interno del servidor.',
        }
    }
}

sc_nuevoDispositivo = {
    'tags': ['principal.py'],
    'parameters': [],
    'responses': {
        '200': {
            'description': 'Dispositivo añadido exitosamente.',
        },
        '302': {
            'description': 'Redirección a la página de inicio de sesión.',
        },
        '401': {
            'description': 'No autorizado.',
        },
        '500': {
            'description': 'Error interno del servidor.',
        }
    }
}

sc_nuevoTemHum = {
    'tags': ['principal.py'],
    'parameters': [],
    'responses': {
        '200': {
            'description': 'Dispositivo añadido exitosamente.',
        },
        '302': {
            'description': 'Redirección a la página de inicio de sesión.',
        },
        '401': {
            'description': 'No autorizado.',
        },
        '500': {
            'description': 'Error interno del servidor.',
        }
    }
}

sc_nuevoAlarma = {
    'tags': ['principal.py'],
    'parameters': [],
    'responses': {
        '200': {
            'description': 'Dispositivo añadido exitosamente.',
        },
        '302': {
            'description': 'Redirección a la página de inicio de sesión.',
        },
        '401': {
            'description': 'No autorizado.',
        },
        '500': {
            'description': 'Error interno del servidor.',
        }
    }
}

sc_nuevoLuzAutomatica = {
    'tags': ['principal.py'],
    'parameters': [],
    'responses': {
        '200': {
            'description': 'Dispositivo añadido exitosamente.',
        },
        '302': {
            'description': 'Redirección a la página de inicio de sesión.',
        },
        '401': {
            'description': 'No autorizado.',
        },
        '500': {
            'description': 'Error interno del servidor.',
        }
    }
}

sc_nuevoCO2 = {
    'tags': ['principal.py'],
    'parameters': [],
    'responses': {
        '200': {
            'description': 'Dispositivo añadido exitosamente.',
        },
        '302': {
            'description': 'Redirección a la página de inicio de sesión.',
        },
        '401': {
            'description': 'No autorizado.',
        },
        '500': {
            'description': 'Error interno del servidor.',
        }
    }
}

sc_borrarDispositivo = {
    'tags': ['principal.py'],
    'parameters': [],
    'responses': {
        '200': {
            'description': 'Dispositivo eliminado exitosamente.',
        },
        '302': {
            'description': 'Redirección a la página de inicio de sesión.',
        },
        '401': {
            'description': 'No autorizado.',
        },
        '500': {
            'description': 'Error interno del servidor.',
        }
    }
}

sc_borrarTemHum = {
    'tags': ['principal.py'],
    'parameters': [],
    'responses': {
        '200': {
            'description': 'Dispositivo eliminado exitosamente.',
        },
        '302': {
            'description': 'Redirección a la página de inicio de sesión.',
        },
        '401': {
            'description': 'No autorizado.',
        },
        '500': {
            'description': 'Error interno del servidor.',
        }
    }
}

sc_borrarAlarma = {
    'tags': ['principal.py'],
    'parameters': [],
    'responses': {
        '200': {
            'description': 'Dispositivo eliminado exitosamente.',
        },
        '302': {
            'description': 'Redirección a la página de inicio de sesión.',
        },
        '401': {
            'description': 'No autorizado.',
        },
        '500': {
            'description': 'Error interno del servidor.',
        }
    }
}

sc_borrarLuzAutomatica = {
    'tags': ['principal.py'],
    'parameters': [],
    'responses': {
        '200': {
            'description': 'Dispositivo eliminado exitosamente.',
        },
        '302': {
            'description': 'Redirección a la página de inicio de sesión.',
        },
        '401': {
            'description': 'No autorizado.',
        },
        '500': {
            'description': 'Error interno del servidor.',
        }
    }
}

sc_borrarCO2 = {
    'tags': ['principal.py'],
    'parameters': [],
    'responses': {
        '200': {
            'description': 'Dispositivo eliminado exitosamente.',
        },
        '302': {
            'description': 'Redirección a la página de inicio de sesión.',
        },
        '401': {
            'description': 'No autorizado.',
        },
        '500': {
            'description': 'Error interno del servidor.',
        }
    }
}

sc_perfil = {
    'tags': ['principal.py'],
    'parameters': [],
    'responses': {
        '200': {
            'description': 'Datos del perfil obtenidos correctamente.',
        },
        '302': {
            'description': 'Redirección a la página de inicio de sesión.',
        },
        '401': {
            'description': 'No autorizado.',
        },
        '500': {
            'description': 'Error interno del servidor.',
        }
    }
}

sc_cambiar = {
    'tags': ['principal.py'],
    'parameters': [],
    'responses': {
        '200': {
            'description': 'Operación exitosa.',
        },
        '302': {
            'description': 'Redirección a la página de inicio de sesión.',
        },
        '401': {
            'description': 'No autorizado.',
        },
        '500': {
            'description': 'Error interno del servidor.',
        }
    }
}

sc_guardarDatos = {
    'tags': ['principal.py'],
    'parameters': [],
    'responses': {
        '200': {
            'description': 'Datos actualizados correctamente.',
        },
        '302': {
            'description': 'Redirección a la página de inicio de sesión.',
        },
        '401': {
            'description': 'No autorizado.',
        },
        '500': {
            'description': 'Error interno del servidor.',
        }
    }
}

#-------------------------------------------------------------
#                   sensores.py
#-------------------------------------------------------------
sc_conectar = {
    'tags': ['sensor.py'],
    'responses': {
        '200': {
            'description': 'Conexión a la alarma realizada correctamente.'
        },
        '500': {
            'description': 'Error interno del servidor.'
        }
    }
}

sc_desconectar = {
    'tags': ['sensor.py'],
    'responses': {
        '200': {
            'description': 'Desconexión de la alarma realizada correctamente.'
        },
        '500': {
            'description': 'Error interno del servidor.'
        }
    }
}

sc_activarMotorCO2 = {
    'tags': ['sensor.py'],
    'responses': {
        '200': {
            'description': 'Motor CO2 activado correctamente.'
        },
        '500': {
            'description': 'Error interno del servidor.'
        }
    }
}

sc_desactivarMotorCO2 = {
    'tags': ['sensor.py'],
    'responses': {
        '200': {
            'description': 'Motor CO2 desactivado correctamente.'
        },
        '500': {
            'description': 'Error interno del servidor.'
        }
    }
}

sc_activarServoCO2 = {
    'tags': ['sensor.py'],
    'responses': {
        '200': {
            'description': 'Servo CO2 activado correctamente.'
        },
        '500': {
            'description': 'Error interno del servidor.'
        }
    }
}

sc_desactivarServoCO2 = {
    'tags': ['sensor.py'],
    'responses': {
        '200': {
            'description': 'Servo CO2 desactivado correctamente.'
        },
        '500': {
            'description': 'Error interno del servidor.'
        }
    }
}

sc_configurarExtractor = {
    'tags': ['sensor.py'],
    'parameters': [
        {
            'name': 'input1',
            'in': 'formData',
            'type': 'string',
            'required': True,
            'description': 'Valor para el salto del extractor'
        },
        {
            'name': 'input2',
            'in': 'formData',
            'type': 'string',
            'required': True,
            'description': 'Valor para la meta del extractor'
        }
    ],
    'responses': {
        '200': {
            'description': 'Configuración del extractor guardada correctamente.'
        },
        '500': {
            'description': 'Error interno del servidor.'
        }
    }
}

sc_configurarVentana = {
    'tags': ['sensor.py'],
    'parameters': [
        {
            'name': 'input3',
            'in': 'formData',
            'type': 'string',
            'required': True,
            'description': 'Valor para el salto de la ventana'
        },
        {
            'name': 'input4',
            'in': 'formData',
            'type': 'string',
            'required': True,
            'description': 'Valor para la meta de la ventana'
        }
    ],
    'responses': {
        '200': {
            'description': 'Configuración de la ventana guardada correctamente.'
        },
        '500': {
            'description': 'Error interno del servidor.'
        }
    }
}

sc_activarCalefaccion = {
    'tags': ['sensor.py'],
    'description': 'Activa la calefacción y guarda el estado actual en MongoDB y MySQL.',
    'responses': {
        '200': {
            'description': 'Calefacción activada correctamente.'
        },
        '500': {
            'description': 'Error interno en el servidor.'
        }
    }
}

sc_desactivarCalefaccion = {
    'tags': ['sensor.py'],
    'description': 'Desactiva la calefacción y guarda el estado actual en MongoDB y MySQL.',
    'responses': {
        '200': {
            'description': 'Calefacción desactivada correctamente.'
        },
        '500': {
            'description': 'Error interno en el servidor.'
        }
    }
}

sc_activarAire = {
    'tags': ['sensor.py'],
    'description': 'Activa el aire acondicionado y guarda el estado actual en MongoDB y MySQL.',
    'responses': {
        '200': {
            'description': 'Aire acondicionado activado correctamente.'
        },
        '500': {
            'description': 'Error interno en el servidor.'
        }
    }
}

sc_desactivarAire = {
    'tags': ['sensor.py'],
    'description': 'Desactiva el aire acondicionado y guarda el estado actual en MongoDB y MySQL.',
    'responses': {
        '200': {
            'description': 'Aire acondicionado desactivado correctamente.'
        },
        '500': {
            'description': 'Error interno en el servidor.'
        }
    }
}

sc_configurarCalefaccion = {
    'tags': ['sensor.py'],
    'description': 'Configura la calefacción con nuevos valores y actualiza en MongoDB y MySQL.',
    'parameters': [
        {
            'name': 'input1',
            'in': 'formData',
            'type': 'string',
            'required': True,
            'description': 'Nuevo valor de salto para la calefacción.'
        },
        {
            'name': 'input2',
            'in': 'formData',
            'type': 'string',
            'required': True,
            'description': 'Nueva meta para la calefacción.'
        }
    ],
    'responses': {
        '200': {
            'description': 'Configuración de calefacción actualizada correctamente.'
        },
        '500': {
            'description': 'Error interno en el servidor.'
        }
    }
}

sc_configurarAire = {
    'tags': ['sensor.py'],
    'description': 'Configura el aire acondicionado con nuevos valores y actualiza en MongoDB y MySQL.',
    'parameters': [
        {
            'name': 'input3',
            'in': 'formData',
            'type': 'string',
            'required': True,
            'description': 'Nuevo valor de salto para el aire acondicionado.'
        },
        {
            'name': 'input4',
            'in': 'formData',
            'type': 'string',
            'required': True,
            'description': 'Nueva meta para el aire acondicionado.'
        }
    ],
    'responses': {
        '200': {
            'description': 'Configuración de aire acondicionado actualizada correctamente.'
        },
        '500': {
            'description': 'Error interno en el servidor.'
        }
    }
}

sc_manual = {
    'tags': ['sensor.py'],
    'description': 'Configura la luz en modo manual y actualiza el estado en MySQL.',
    'responses': {
        '200': {
            'description': 'Configuración de luz cambiada a manual correctamente.'
        },
        '500': {
            'description': 'Error interno en el servidor.'
        }
    }
}

sc_automatica = {
    'tags': ['sensor.py'],
    'description': 'Configura la luz en modo automático y actualiza el estado en MySQL.',
    'responses': {
        '200': {
            'description': 'Configuración de luz cambiada a automática correctamente.'
        },
        '500': {
            'description': 'Error interno en el servidor.'
        }
    }
}

sc_encender = {
    'tags': ['sensor.py'],
    'description': 'Enciende la luz automáticamente y actualiza el estado en MongoDB y MySQL.',
    'responses': {
        '200': {
            'description': 'Luz encendida correctamente.'
        },
        '500': {
            'description': 'Error interno en el servidor.'
        }
    }
}

sc_apagar = {
    'tags': ['sensor.py'],
    'description': 'Apaga la luz automáticamente y actualiza el estado en MongoDB y MySQL.',
    'responses': {
        '200': {
            'description': 'Luz apagada correctamente.'
        },
        '500': {
            'description': 'Error interno en el servidor.'
        }
    }
}

sc_configurarLuz = {
    'tags': ['sensor.py'],
    'description': 'Configura la luminosidad de la luz automáticamente y actualiza en MongoDB y MySQL.',
    'parameters': [
        {
            'name': 'input1',
            'in': 'formData',
            'type': 'string',
            'required': True,
            'description': 'Nuevo valor de luminosidad para la luz.'
        }
    ],
    'responses': {
        '200': {
            'description': 'Configuración de luminosidad de la luz actualizada correctamente.'
        },
        '500': {
            'description': 'Error interno en el servidor.'
        }
    }
}
