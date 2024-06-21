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

INSERT INTO api_producto (nombre, descripcion, precio, stock, categoria_id, bodega_id, estado) VALUES
    ('Aceite de Motor', 'Aceite para motor de alta calidad', 200000, 100, 1, 1, 1),
    ('Filtro de Aire', 'Filtro de aire eficiente', 15000, 50, 1, 1, 1),
    ('Turbo de Motor', 'Turbo de alto rendimiento', 100000, 20, 1, 1, 1),
    ('Parachoques delantero', 'Parachoques delantero resistente', 200000, 50, 2, 2, 1),
    ('Parachoques trasero', 'Parachoques trasero resistente', 150000, 30, 2, 2, 1),
    ('Vidrio delantero', 'Vidrio delantero templado', 50000, 100, 2, 1, 1),
    ('Vidrio trasero', 'Vidrio trasero templado', 50000, 80, 2, 1, 1),
    ('Amortiguador delantero', 'Amortiguador delantero de alta calidad', 80000, 50, 3, 1, 1),
    ('Amortiguador trasero', 'Amortiguador trasero de alta calidad', 80000, 50, 3, 1, 1),
    ('Disco de Freno delantero', 'Disco de freno delantero duradero', 50000, 30, 4, 1, 1),
    ('Disco de Freno trasero', 'Disco de freno trasero duradero', 50000, 30, 4, 1, 1),
    ('Sistema de Inyección Electrónica', 'Sistema de inyección electrónica avanzado', 300.00, 20, 5, 2, 1),
    ('Navegador GPS', 'Navegador GPS de última generación', 350000, 15, 5, 2, 1),
    ('Alternador de Motor', 'Alternador de motor de alta eficiencia', 150000, 20, 1, 1, 1),
    ('Batería de Motor', 'Batería de motor duradera', 100000, 10, 1, 1, 1),
    ('Llantas de Aluminio', 'Llantas de aluminio ligeras', 200000, 30, 2, 2, 1),
    ('Bomba de Combustible', 'Bomba de combustible eficiente', 100000, 20, 1, 1, 1),
    ('Caja de Cambios', 'Caja de cambios robusta', 200000, 10, 1, 1, 1),
    ('Motor de Arranque', 'Motor de arranque de alta potencia', 150000, 5, 1, 1, 1),
    ('Caja de Velocidades', 'Caja de velocidades precisa', 100000, 15, 1, 1, 1);


INSERT INTO api_promocion (descripcion, descuento, fecha_inicio, fecha_fin, estado) VALUES
    ('Promoción de verano', 10, '2024-12-01', '2025-02-28', 1),
    ('Promoción de invierno', 15, '2024-06-21', '2024-06-23', 1);

INSERT INTO api_promocion_productos (promocion_id, producto_id) VALUES
(1, 1),
(1, 2),
(2, 3),
(2, 4);
