package kubernetes.admission

deny[msg] {
    input.request.kind.kind == "Pod"
    some i
    image := input.request.object.spec.containers[i].image
    not startswith(image, "gcr.io/")
    msg := sprintf("image '%v' comes from an untrusted registry", [image])
}
