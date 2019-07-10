def polyfit_rev_bas():
	df = pd.DataFrame({'nr':beers.num_reviews,'ba':beers.BAscore}).sort_values('nr')
	x = df.nr.values
	y = df.ba.values

	# calculate polynomial
	z = np.polyfit(x, y, 4)
	f = np.poly1d(z)
	f_text = ' + '.join(['{:0.3e}X^{}'.format(f[x],x) for x in range(len(f)+1)])


	# calculate new x's and y's
	x_fit = np.linspace(x[0], x[-1], 50)
	y_fit = f(x_fit)

	trace1 = go.Scatter(
	                  x=x,
	                  y=y,
	                  mode='markers',
	                  marker=go.Marker(color='rgb(255, 127, 14)'),
	                  name='Data'
	                  )
	trace2 = go.Scatter(
	                  x=x_fit,
	                  y=y_fit,
	                  mode='lines',
	                  marker=go.Marker(color='rgb(31, 119, 180)'),
	                  name='Fit',
	                  text ='3d-PolyFit:{}'.format(f_text),
	                  textposition = 'bottom center',
	                  textfont=dict(
	                          family='sans serif',
	                          size=18,
	                          color='#ff7f0e'
	                          )
	                  )

	layout = go.Layout(
	                title='Number of Reviews v. Beer Advocate Score',
	                plot_bgcolor='rgb(229, 229, 229)',
	                xaxis=go.XAxis(zerolinecolor='rgb(255,255,255)', gridcolor='rgb(255,255,255)'),
	                yaxis=go.YAxis(zerolinecolor='rgb(255,255,255)', gridcolor='rgb(255,255,255)'),
	                showlegend=False
	                )


	data=[trace1,trace2]
	fig = go.Figure(data=data,layout=layout)
	return py.offline.iplot(fig)




"""
# Creating the dataset, and generating the plot
trace1 = go.Scatter(
                  x=x,
                  y=y,
                  mode='markers',
                  marker=go.Marker(color='rgb(255, 127, 14)'),
                  name='Data'
                  )

trace2 = go.Scatter(
                  x=x_new,
                  y=y_new,
                  mode='lines',
                  marker=go.Marker(color='rgb(31, 119, 180)'),
                  name='Fit'
                  )

annotation = go.Annotation(
                  x=6,
                  y=-4.5,
                  text='$\textbf{Fit}: 0.43X^3 - 0.56X^2 + 16.78X + 10.61$',
                  showarrow=False
                  )
layout = go.Layout(
                title='Polynomial Fit in Python',
                plot_bgcolor='rgb(229, 229, 229)',
                xaxis=go.XAxis(zerolinecolor='rgb(255,255,255)', gridcolor='rgb(255,255,255)'),
                yaxis=go.YAxis(zerolinecolor='rgb(255,255,255)', gridcolor='rgb(255,255,255)'),
                annotations=[annotation]
                )

data = [trace1, trace2]
fig = go.Figure(data=data, layout=layout)

py.plot(fig, filename='Polynomial-Fit-in-python')
"""