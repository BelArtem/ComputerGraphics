# Code review.

## Выполнил Белоус Артем

Код брался из репозитория:

[https://github.com/ZapWay/cg3](https://github.com/ZapWay/cg3)

1. Архитектура приложения показалась мне достаточно сложной. Например, основной функцией приложения является функция `Canvas` , которая занимает 289 строк.  Далее, в этой функции реализуется функция `useEffect`, в которой реализуется еще одна функция `redraw`. Помимо `useEffect`, в `Canvas` также содержатся  `getGridCoordinates, handleScaleCahnge, handleCanvasClick, drawGrid, drawBresenhamLine, drawDDALine, drawBresenhamCircle, drawMidpointCircle, drawCirclePoints` .  Таким образом, основная функция получается крайне перегруженной. Это можно побороть, например, путем вынесения определения функций из тела основной функции. Также происходит смешение различных уровней абстракций. Например, работа с отображением фигур смешивается с непосредственной реализацией алгоритмов растеризации линий. Чтобы такого смешения не происходило, можно, например, реализовать класс, отвечающий за реализацию алгоритмов растеризации. Однако учитывая небольшой размер приложения, это не критично.  
2. Рассмотрим программу с точки зрения производительности. Для этого рассмотрим функцию `useEffect` :
    
    ```jsx
    useEffect(() => {
        const canvas = canvasRef.current;
        const ctx = canvas.getContext('2d');
        const redraw = () => {
          canvas.width = 400 * scale;
          canvas.height = 400 * scale;
    
          ctx.clearRect(0, 0, canvas.width, canvas.height);
          ctx.scale(scale, scale);
    
          drawGrid(ctx, canvas.width / scale, canvas.height / scale, gridSize);
          if ((algorithm === 'bresenhamLine' || algorithm === 'ddaLine') && lineStart && lineEnd) {
            if (algorithm === 'bresenhamLine') {
              drawBresenhamLine(ctx, lineStart.x, lineStart.y, lineEnd.x, lineEnd.y, gridSize);
            } else {
              drawDDALine(ctx, lineStart.x, lineStart.y, lineEnd.x, lineEnd.y, gridSize);
            }
          } else if ((algorithm === 'bresenhamCircle' || algorithm === 'midpointCircle') && circleCenter && circleRadius !== null) {
            if (algorithm === 'bresenhamCircle') {
              drawBresenhamCircle(ctx, circleCenter.x, circleCenter.y, circleRadius, gridSize);
            } else {
              drawMidpointCircle(ctx, circleCenter.x, circleCenter.y, circleRadius, gridSize);
            }
    
          }
    
        }
    
        ctx.clearRect(0, 0, canvas.width, canvas.height);
    
        drawGrid(ctx, canvas.width, canvas.height, gridSize);
    
        switch (algorithm) {
          case 'bresenhamLine':
            drawBresenhamLine(ctx, lineStart.x, lineStart.y, lineEnd.x, lineEnd.y, gridSize);
            break;
          case 'ddaLine':
            drawDDALine(ctx, lineStart.x, lineStart.y, lineEnd.x, lineEnd.y, gridSize);
            break;
          case 'bresenhamCircle':
            drawBresenhamCircle(ctx, circleCenter.x, circleCenter.y, circleRadius, gridSize);
            break;
          case 'midpointCircle':
            drawMidpointCircle(ctx, circleCenter.x, circleCenter.y, circleRadius, gridSize);
            break;
          default:
            break;
        }
        ctx.setTransform(1, 0, 0, 1, 0, 0);
        redraw(); 
      }, [gridSize, algorithm, lineStart, lineEnd, circleCenter, circleRadius, scale]);
    ```
    
    Можно заметить, что после объявления функции `redraw` происходит очистка холста, перерисовка сетки и рисование линии (либо окружности), после чего происходит вызов `redraw()` . Функция `redraw()` , в свою очередь, опять чистит холст, рисует сетку и необходимую фигуру. 
    
    Таким образом кажется, что почти весь код после определения и перед вызовом функции `redraw()` является излишним.
    
3. Функция `handleScaleCahnge` содержит в своем названии орфографическую ошибку. Ее стоит исправить на `handleScaleChange` .
4. Далее рассмотрим корректность работы приложения.  Из определения функции `handleCanvasClick` видно, что предполагается возможность задания необходимых координат для построения фигур пользователем путем нажатия мышкой на холст. В случае с окружностями функция работает корректно. Однако в случае с линиями происходит ошибка :
    
    ![image.png](image.png)
    
5. Далее рассмотрим функциональность приложения. Приложение не содержит в себе реализацию пошагового алгоритма построения линии. Напомню, что пошаговый алгоритм представляет собой вычисление y-координаты пикселя путем подстановки x-координаты в уравнение прямой $y=kx$. Приращение x-координаты, в свою очередь, должно быть достаточно малым.
    
    Судя по всему, в приложении также отсутствует замер времени работы реализованных алгоритмов. Это можно реализовать путем генерирования датасета из $n$ точек, после чего начать отсчет времени работы каждого алгоритма для каждой из случайно сгенерированных $n$ точек.