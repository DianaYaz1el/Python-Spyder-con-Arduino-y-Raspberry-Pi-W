function seisservosgraf
    % GUI de control de 6 servos con simulación 2D

    global s angulos;

    % Conexión al Arduino
    s = serialport('COM22',9600);
    pause(2);

    % Ángulos iniciales [S1,S2,S3,S4,S5,S6]
    angulos = [90 90 0 180 90 90];

    % Crear ventana UI
    fig = uifigure('Name','Control de 6 Servos + Simulación','Position',[100 100 900 550]);
    ax  = uiaxes(fig,'Position',[450 100 400 400]);
    ax.Title.String   = 'Simulación del Brazo';
    ax.XLabel.String  = 'X (cm)';
    ax.YLabel.String  = 'Y (cm)';
    ax.XLim = [-20 20];
    ax.YLim = [-20 30];
    axis(ax,'equal');
    grid(ax,'on');

    % Crear sliders dinámicos para cada servo
    for i = 1:6
        y_pos = 500 - i*60;
        uilabel(fig,'Position',[30 y_pos 60 22],'Text',['Servo ' num2str(i)]);
        if i == 6
            lim = [0 90]; ticks = 0:15:90;
        else
            lim = [0 180]; ticks = 0:30:180;
        end
        uislider(fig,...
            'Limits',lim,...
            'MajorTicks',ticks,...
            'Value',angulos(i),...
            'ValueChangedFcn',@(src,evt)moverServo(i,round(src.Value)),...
            'Position',[100 y_pos 250 3]);
    end

    % Enviar configuración inicial y dibujar
    enviarYAlojar();
    dibujarBrazo();

    % ------- Funciones anidadas -------

    function moverServo(id, val)
        % Actualiza ángulo y refresca dibujo y Arduino
        angulos(id) = val;
        enviarYAlojar();
        dibujarBrazo();
    end

    function enviarYAlojar()
        % Envía la cadena de ángulos al Arduino
        str = join(string(angulos),',');
        writeline(s,str);
        disp("Ángulos enviados: " + str);
    end

    function dibujarBrazo()
        % Cinemática 2D de servos 2,3,4 y apertura de pinza (6)
        L1 = 8; L2 = 6; L3 = 4; jawLen = 1.5;
        % Ajuste de orientaciones:
        t2 = deg2rad(angulos(2));        % S2 hombro, 90°→vertical arriba
        t3 = deg2rad(90 - angulos(3));   % ← correcto   %t3 = deg2rad(angulos(3) + 90);   % S3 codo   +90° para que 0→izquierda
        t4 = deg2rad(angulos(4) - 90);   % S4 muñeca -90° para que 180→izquierda

        % Puntos de la cadena cinemática
        p0 = [0,0];
        p1 = p0 + L1*[cos(t2),       sin(t2)];
        p2 = p1 + L2*[cos(t2+t3),    sin(t2+t3)];
        p3 = p2 + L3*[cos(t2+t3+t4), sin(t2+t3+t4)];

        % Pinza (servo6 abre la U)
        openA = deg2rad(angulos(6));
        dirG  = [cos(t2+t3+t4), sin(t2+t3+t4)];
        orth  = [-dirG(2), dirG(1)];
        pA    = p3 + jawLen*(dirG*cos(openA) + orth*sin(openA));
        pB    = p3 + jawLen*(dirG*cos(openA) - orth*sin(openA));

        % Dibujar nuevamente
        cla(ax); hold(ax,'on');
        ax.XLim = [-20 20]; ax.YLim = [-20 30];
        grid(ax,'on'); axis(ax,'equal');
        % Eslabones verdes
        plot(ax,[p0(1) p1(1) p2(1) p3(1)], [p0(2) p1(2) p2(2) p3(2)], ...
             '-o','LineWidth',6,'Color',[0 .5 0],'MarkerFaceColor',[0 .7 0]);
        % Pinza
        plot(ax,[p3(1) pA(1)], [p3(2) pA(2)], '-', 'LineWidth',6,'Color',[0 .5 0]);
        plot(ax,[p3(1) pB(1)], [p3(2) pB(2)], '-', 'LineWidth',6,'Color',[0 .5 0]);
        hold(ax,'off');
    end
end
 