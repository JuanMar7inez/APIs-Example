function buscarPorCodigo() {
    const codigo = document.getElementById("codigoInput").value;
    const soapEnvelope =
      `<?xml version="1.0"?>
      <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:edu="edu.soap.cursos">
        <soapenv:Header/>
        <soapenv:Body>
          <edu:getCursoPorCodigo>
            <codigo>${codigo}</codigo>
          </edu:getCursoPorCodigo>
        </soapenv:Body>
      </soapenv:Envelope>`;

    fetch('http://127.0.0.1:8000/', {
      method: 'POST',
      headers: {
        'Content-Type': 'text/xml;charset=UTF-8',
        'SOAPAction': ''
      },
      body: soapEnvelope
    })
    .then(res => res.text())
    .then(str => {
      const parser = new DOMParser();
      const xml = parser.parseFromString(str, "text/xml");
      console.log(xml.documentElement.outerHTML); // Para debug

      const nombre = xml.getElementsByTagName("tns:nombre")[0]?.textContent;
      const codigo = xml.getElementsByTagName("tns:codigo")[0]?.textContent;
      const id = xml.getElementsByTagName("tns:id")[0]?.textContent;

      if (nombre && id !== "-1") {
        document.getElementById("resultadoSOAP").innerText = `Curso: ${nombre} (${codigo}) ID: ${id}`;
      } else {
        document.getElementById("resultadoSOAP").innerText = "Curso no encontrado";
      }
    })
    .catch(err => console.error("Error SOAP:", err));
  }

  function listarCursos() {
    fetch('http://127.0.0.1:5000/cursos')
      .then(response => response.json())
      .then(data => {
        const lista = document.getElementById("listaCursos");
        lista.innerHTML = "";
        data.forEach(curso => {
          const li = document.createElement("li");
          li.textContent = `${curso.nombre} (${curso.codigo})`;
          lista.appendChild(li);
        });
      });
  }