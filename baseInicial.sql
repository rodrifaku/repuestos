INSERT INTO api_sucursal (nombre, direccion, estado) VALUES
    ('San Bernardo','Freire 140',1),
    ('Santiago','Alameda 1234',1),
    ('Melipilla','Caldera 4321',1);

INSERT INTO api_bodega (nombre, sucursal_id, direccion, estado) VALUES
    ('Bodega Central', 1, 'Dirección de la Bodega Central', 1),
    ('Bodega Norte', 2, 'Dirección de la Bodega Norte', 1);

INSERT INTO api_categoria (nombre, descripcion, estado) VALUES
    ('Motor', 'Productos relacionados con el motor del automóvil',1),
    ('Carrocería', 'Productos relacionados con la estructura y la apariencia del automóvil',1),
    ('Suspensión', 'Productos relacionados con la suspensión del automóvil',1),
    ('Frenos', 'Productos relacionados con los sistemas de frenos del automóvil',1),
    ('Electrónica', 'Productos relacionados con la electrónica del automóvil',1);

INSERT INTO api_producto (nombre,descripcion,precio,stock,estado,categoria_id,bodega_id,descuento_id) VALUES
	 ('Aceite de Motor','Aceite para motor de alta calidad',20,97,1,1,1,NULL),
	 ('Filtro de Aire','Filtro de aire eficiente',15,45,1,1,1,NULL),
	 ('Turbo de Motor','Turbo de alto rendimiento',100,20,1,1,1,NULL),
	 ('Parachoques delantero','Parachoques delantero resistente',200,16,1,2,2,NULL),
	 ('Parachoques trasero','Parachoques trasero resistente',150,12,1,2,2,NULL),
	 ('Vidrio delantero','Vidrio delantero templado',50,100,1,2,1,NULL),
	 ('Vidrio trasero','Vidrio trasero templado',50,76,1,2,1,NULL),
	 ('Amortiguador delantero','Amortiguador delantero de alta calidad',80,50,1,3,1,NULL),
	 ('Amortiguador trasero','Amortiguador trasero de alta calidad',80,42,1,3,1,NULL),
	 ('Disco de Freno delantero','Disco de freno delantero duradero',50,30,1,4,1,NULL),
	 ('Disco de Freno trasero','Disco de freno trasero duradero',50,30,1,4,1,NULL),
	 ('Sistema de Inyección Electrónica','Sistema de inyección electrónica avanzado',300,20,1,5,2,NULL),
	 ('Navegador GPS','Navegador GPS de última generación',350,15,1,5,2,NULL),
	 ('Alternador de Motor','Alternador de motor de alta eficiencia',150,20,1,1,1,NULL),
	 ('Batería de Motor','Batería de motor duradera',100,10,1,1,1,NULL),
	 ('Llantas de Aluminio','Llantas de aluminio ligeras',200,30,1,2,2,NULL),
	 ('Bomba de Combustible','Bomba de combustible eficiente',100,20,1,1,1,NULL),
	 ('Caja de Cambios','Caja de cambios robusta',200,10,1,1,1,NULL),
	 ('Motor de Arranque','Motor de arranque de alta potencia',150,5,1,1,1,NULL),
	 ('Caja de Velocidades','Caja de velocidades precisa',100,15,1,1,1,NULL),
	 ('otro2','Descripción del producto nuevo',99.99,10,1,4,1,NULL),
	 ('otro3','Descripción del producto nuevo',99.99,10,1,4,1,NULL);



INSERT INTO api_promocion (descripcion, descuento, fecha_inicio, fecha_fin, estado) VALUES
    ('Promoción de verano', 10, '2024-12-01', '2025-02-28', 1),
    ('Promoción de invierno', 15, '2024-06-21', '2024-06-23', 1);

INSERT INTO api_promocion_productos (promocion_id, producto_id) VALUES
(1, 1),
(1, 2),
(2, 3),
(2, 4);
