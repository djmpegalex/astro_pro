def trnzit_gog(x_tranzit):
    if 0 <= x_tranzit <= 1300:
        date_percent = coords_date(x_tranzit)

        # contents = output_map_vargas_str.getvalue()

        labl_poz.place(x=x_tranzit+100, y=78, width=1, height=308)


        last_num = txt_lastDate.get()
        last_num = datetime.strptime(last_num, FORMAT_DATE)
        delta_date = last_num + timedelta(days=date_percent)
        new_date_tranzit = str(delta_date.day) + "." + str(delta_date.month) + "." + str(delta_date.year)
        new_date_tranzit = datetime.strptime(new_date_tranzit, FORMAT_DATE)
        new_date_tranzit = new_date_tranzit.strftime(FORMAT_DATE)

        planet_in_tranzit = calculateTranzitMap.calculate_tranzit_map(new_date_tranzit, txtDate.get(), txtTime.get())
        graha_in_degrees_transit = planet_in_tranzit.graha_in_degrees_transit

        graha_in_degrees = planet_in_tranzit.graha_in_degrees

        natal_moon = int(planet_in_tranzit.natal_moon_degrees / 108000)

        """
            построение карты транзитов по накшатрам
        """

        ax_bh.cla()
        ax_bh.plot(0, 0, '-b', linewidth=0.1, markersize=0)
        ax_bh.plot(1, 1, '-b', linewidth=0.1, markersize=0)


        for x1, y1, z1, x2, y2 in zip(nak_x, nak_y, nak_z, nak_xl, nak_yl):
            ax_bh.plot([0, x1], [0, y1], color='blue', lw=.2)
            ax_bh.text(x2, y2, '%d' % (int(z1 + 1)), horizontalalignment='center',
                     verticalalignment='center', rotation=0, color=nak_clrr[nak_ccc[z1] + 1], size=8)

        for dgr, nam, r in zip(graha_in_degrees, nak_nam_pl, nak_rr):
            dgr0 = dgr / 1296000 * 2 * 3.141
            xx = np.cos(dgr0) * r
            yy = np.sin(dgr0) * r
            ax_bh.plot(xx, yy, '.', color='black', lw=.2)
            ax_bh.text(xx - abs(xx * .02), yy + abs(yy * .03), nam, verticalalignment='bottom',
                     horizontalalignment='center', size=6)




        ax_sud.cla()
        ax_sud.plot(0, 0, '-b', linewidth=0.1, markersize=0)
        ax_sud.plot(100, 100, '-b', linewidth=0.1, markersize=0)

        def brilliant_map(i):
            l = mlines.Line2D([BRILLANT_MAP_X[i * 2], BRILLANT_MAP_X[i * 2 + 1]],
                              [BRILLANT_MAP_Y[i * 2], BRILLANT_MAP_Y[i * 2 + 1]], linewidth=1.0)
            l.set_color("blue")
            ax_sud.add_line(l)

        list(map(lambda u: brilliant_map(u), MAP_RANGE))

        l = mlines.Line2D(COORDS_BHAVAS_X, COORDS_BHAVAS_Y, linewidth=1.0)
        l.set_color("blue")
        ax_sud.add_line(l)

        def output_tranzit(nm):
            n = int(nm / 7)
            house = math.trunc(graha_in_degrees_transit[nm] / DEGREES_IN_ZNAK)
            i = (graha_in_degrees_transit[nm] - (house * DEGREES_IN_ZNAK)) * 3

            point_OX = COORDS_BHAVAS_X[house]
            point_OY = COORDS_BHAVAS_Y[house]
            radius = 14 + (n * 1.5)
            angle = ANGLES[house]

            if next_range[house] == 0:
                x = (radius * math.sin(math.radians(i + angle))) + point_OX
                y = (radius * math.cos(math.radians(i + angle))) + point_OY
            else:
                x = (radius * math.cos(math.radians(i + angle))) + point_OX
                y = (radius * math.sin(math.radians(i + angle))) + point_OY
            delta_OX = DELTA_OX_TEXT[house]
            delta_OY = DELTA_OY_TEXT[house]

            if (int(nm / 7)) == (nm / 7):
                ax_sud.text(x + delta_OX - .4, y + delta_OY - .4, NAME_PLANETS[n], color="black",
                            size=8)
                ax_sud.text(x + delta_OX, y + delta_OY, NAME_PLANETS[n], color=COLOR_PLANET[n], size=8)

                l = mlines.Line2D([x, x + .1], [y, y + .1], linewidth=3)
                l.set_color("black")
                ax_sud.add_line(l)
            else:
                ax_sud.text(x + delta_OX - .4, y + delta_OY - .4, NAME_PLANETS[n], color="gray",
                            size=8)
                ax_sud.text(x + delta_OX, y + delta_OY, NAME_PLANETS[n], color=COLOR_PLANET_ASPECT[n], size=8)

        list(map(lambda y: output_tranzit(y), ASPECTS_RANGE))

        def text_znak(i):
            number_znak_sud = int(math.fmod((natal_moon + i), ZNAKS_IN_ZODIAK))
            OX = HOUSE_OX[i]
            OY = HOUSE_OY[i]
            ax_sud.text(OX + DELTA_P[number_znak_sud], OY, str(number_znak_sud + 1), color="black", size=10)
            ax_sud.text(OX + .4 + DELTA_P[number_znak_sud], OY + .4, str(number_znak_sud + 1),
                        color=COLOR_ELEMENTS_ZNAK[number_znak_sud], size=10)

        list(map(lambda x: text_znak(x), ZODIAK_RANGE))

        labl_tranzit.config(text=new_date_tranzit)
        lx_tranzit.delete(0, END)
        lx_tranzit.insert(0, x_tranzit)

        canvasAgg_sud.draw()
        canvas_sud = canvasAgg_sud.get_tk_widget()
        canvas_sud.pack(fill=BOTH, expand=1)
        frm_sud.pack(fill=BOTH, expand=1)

        canvasAgg_bh.draw()
        canvas_bh = canvasAgg_bh.get_tk_widget()
        canvas_bh.pack(fill=BOTH, expand=1)
        frm_bh.pack(fill=BOTH, expand=1)